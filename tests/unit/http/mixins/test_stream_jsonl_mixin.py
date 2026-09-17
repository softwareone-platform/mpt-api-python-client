import inspect
import json
from contextlib import aclosing

import httpx
import pytest
import respx

from mpt_api_client import RQLQuery
from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import AsyncStreamJSONLMixin, StreamJSONLMixin
from tests.unit.conftest import API_URL, DummyModel
from tests.unit.http.conftest import (
    JSON_LEGAL_IN_STRING,
    KEEPALIVE_LINE,
    NON_OBJECT_LINE_CASES,
    UNDECODABLE_LINES,
    AsyncRecordingProgress,
    ClosableAsyncByteStream,
    ClosableByteStream,
    RecordingProgress,
)

JSONL_BODY = b'{"id": "ID-1", "name": "Charge 1"}\n\n{"id": "ID-2", "name": "Charge 2"}\n'
MALFORMED_JSONL_BODY = b'not-json\n{"id": "ID-1", "name": "Charge 1"}\n'


def separator_jsonl_response(separator):
    body = f'{{"id": "ID-1", "name": "a{separator}b"}}\n'.encode()
    return httpx.Response(httpx.codes.OK, content=body)


def raw_line_response(line):
    return httpx.Response(httpx.codes.OK, content=f"{line}\n".encode())


def two_records_around(line):
    body = f'{{"id": "ID-1"}}\n{line}\n{{"id": "ID-2"}}\n'.encode()
    return httpx.Response(httpx.codes.OK, content=body)


class DummyStreamJSONLService(
    StreamJSONLMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/api/v1/charges"
    _model_class = DummyModel


class AsyncDummyStreamJSONLService(
    AsyncStreamJSONLMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/api/v1/charges"
    _model_class = DummyModel


@pytest.fixture
def stream_service(http_client):
    return DummyStreamJSONLService(http_client=http_client)


@pytest.fixture
def async_stream_service(async_http_client):
    return AsyncDummyStreamJSONLService(http_client=async_http_client)


@respx.mock
def test_stream_yields_models(stream_service):
    route = respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=JSONL_BODY)
    )

    result = list(stream_service.stream())

    request = route.calls[0].request
    assert [charge.id for charge in result] == ["ID-1", "ID-2"]
    assert all(isinstance(charge, DummyModel) for charge in result)
    assert request.headers["Accept"] == "application/jsonl"


@pytest.mark.parametrize("separator", JSON_LEGAL_IN_STRING)
@respx.mock
def test_stream_keeps_json_legal_separator(stream_service, separator):
    expected_pair = ("ID-1", f"a{separator}b")
    respx.get(f"{API_URL}/api/v1/charges").mock(return_value=separator_jsonl_response(separator))

    result = list(stream_service.stream())

    assert [(charge.id, charge.name) for charge in result] == [expected_pair]


@respx.mock
def test_stream_applies_query_filters(stream_service):
    route = respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=JSONL_BODY)
    )

    result = list(stream_service.filter(RQLQuery(status="active")).stream())

    request = route.calls[0].request
    assert result
    assert "status" in request.url.query.decode()


@respx.mock
def test_stream_progress_events(stream_service, recording_progress: RecordingProgress):
    respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=JSONL_BODY)
    )

    list(stream_service.stream(progress=recording_progress))  # act

    assert recording_progress.events == [
        ("item_processed",),
        ("item_processed",),
        ("completed",),
    ]


@respx.mock
def test_stream_progress_early_break(stream_service, recording_progress: RecordingProgress):
    respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=JSONL_BODY)
    )
    iterator = stream_service.stream(progress=recording_progress)
    next(iterator)

    iterator.close()  # act

    assert recording_progress.events == [("item_processed",)]


@respx.mock
def test_stream_progress_bad_line(stream_service, recording_progress: RecordingProgress):
    respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=MALFORMED_JSONL_BODY)
    )
    iterator = stream_service.stream(progress=recording_progress)

    with pytest.raises(ValueError, match="Expecting value"):
        next(iterator)

    assert recording_progress.events == []


@pytest.mark.parametrize("line", NON_OBJECT_LINE_CASES)
@respx.mock
def test_stream_rejects_non_object_line(stream_service, line):
    respx.get(f"{API_URL}/api/v1/charges").mock(return_value=raw_line_response(line))
    iterator = stream_service.stream()

    with pytest.raises(json.JSONDecodeError, match="record must be an object"):
        next(iterator)


@respx.mock
def test_stream_skips_whitespace_keepalive(stream_service):
    respx.get(f"{API_URL}/api/v1/charges").mock(return_value=two_records_around(KEEPALIVE_LINE))

    result = list(stream_service.stream())

    assert [charge.id for charge in result] == ["ID-1", "ID-2"]


@pytest.mark.parametrize(("line", "decode_error"), UNDECODABLE_LINES)
@respx.mock
def test_stream_rejects_non_record_line(stream_service, line, decode_error):
    respx.get(f"{API_URL}/api/v1/charges").mock(return_value=raw_line_response(line))
    iterator = stream_service.stream()

    with pytest.raises(json.JSONDecodeError, match=decode_error):
        next(iterator)


@respx.mock
async def test_async_stream_yields_models(async_stream_service):
    route = respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=JSONL_BODY)
    )

    result = [charge async for charge in async_stream_service.stream()]

    request = route.calls[0].request
    assert [charge.id for charge in result] == ["ID-1", "ID-2"]
    assert all(isinstance(charge, DummyModel) for charge in result)
    assert request.headers["Accept"] == "application/jsonl"


@pytest.mark.parametrize("separator", JSON_LEGAL_IN_STRING)
@respx.mock
async def test_async_stream_keeps_separator(async_stream_service, separator):
    expected_pair = ("ID-1", f"a{separator}b")
    respx.get(f"{API_URL}/api/v1/charges").mock(return_value=separator_jsonl_response(separator))

    result = [charge async for charge in async_stream_service.stream()]

    assert [(charge.id, charge.name) for charge in result] == [expected_pair]


@respx.mock
async def test_async_stream_progress_events(
    async_stream_service, async_recording_progress: AsyncRecordingProgress
):
    respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=JSONL_BODY)
    )

    [charge async for charge in async_stream_service.stream(progress=async_recording_progress)]

    assert async_recording_progress.events == [
        ("item_processed",),
        ("item_processed",),
        ("completed",),
    ]


@respx.mock
async def test_async_stream_progress_early_break(
    async_stream_service, async_recording_progress: AsyncRecordingProgress
):
    respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=JSONL_BODY)
    )
    iterator = async_stream_service.stream(progress=async_recording_progress)

    await anext(iterator)
    await iterator.aclose()

    assert async_recording_progress.events == [("item_processed",)]


@respx.mock
async def test_async_stream_progress_bad_line(
    async_stream_service, async_recording_progress: AsyncRecordingProgress
):
    respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=MALFORMED_JSONL_BODY)
    )
    iterator = async_stream_service.stream(progress=async_recording_progress)

    with pytest.raises(ValueError, match="Expecting value"):
        await anext(iterator)

    assert async_recording_progress.events == []


@pytest.mark.parametrize("line", NON_OBJECT_LINE_CASES)
@respx.mock
async def test_async_stream_rejects_non_object(async_stream_service, line):
    respx.get(f"{API_URL}/api/v1/charges").mock(return_value=raw_line_response(line))
    iterator = async_stream_service.stream()

    with pytest.raises(json.JSONDecodeError, match="record must be an object"):
        await anext(iterator)


@respx.mock
async def test_async_jsonl_skips_whitespace_keepalive(async_stream_service):
    respx.get(f"{API_URL}/api/v1/charges").mock(return_value=two_records_around(KEEPALIVE_LINE))

    async with aclosing(async_stream_service.stream()) as records:
        result = [charge.id async for charge in records]

    assert result == ["ID-1", "ID-2"]


@pytest.mark.parametrize(("line", "decode_error"), UNDECODABLE_LINES)
@respx.mock
async def test_async_jsonl_rejects_non_record_line(async_stream_service, line, decode_error):
    respx.get(f"{API_URL}/api/v1/charges").mock(return_value=raw_line_response(line))
    iterator = async_stream_service.stream()

    with pytest.raises(json.JSONDecodeError, match=decode_error):
        await anext(iterator)


@respx.mock
def test_stream_break_releases_body(stream_service):
    # The sync twin needs no explicit close: dropping the suspended generator closes it.
    body = ClosableByteStream(JSONL_BODY)
    respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, stream=body)
    )
    consumed = []

    for record in stream_service.stream():  # act
        consumed.append(record.id)
        break

    assert (consumed, body.closed) == (["ID-1"], True)


@respx.mock
async def test_async_jsonl_aclosing_releases_body(async_stream_service):
    # An abandoned async generator is finalized by the event loop's async-generator hook,
    # so only an explicit close releases the response at a point the caller controls.
    body = ClosableAsyncByteStream(JSONL_BODY)
    respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, stream=body)
    )
    consumed = []

    async with aclosing(async_stream_service.stream()) as records:  # act
        async for record in records:
            consumed.append(record.id)
            break

    assert (consumed, body.closed) == (["ID-1"], True)


# 6.4.0 published stream(progress=...) and nothing else. 7.0.0 renamed it to stream_jsonl()
# and handed the freed name to the platform streaming read, silently changing what a 6.x
# call did. Pin the signature so the name cannot drift again without a test failing.
@pytest.mark.parametrize(
    ("mixin", "is_async"),
    [
        pytest.param(StreamJSONLMixin, False, id="sync"),
        pytest.param(AsyncStreamJSONLMixin, True, id="async"),
    ],
)
def test_stream_keeps_the_published_signature(mixin, is_async):
    signature = inspect.signature(mixin.stream)
    progress = signature.parameters["progress"]

    result = (
        list(signature.parameters),
        progress.kind,
        progress.default,
        inspect.isasyncgenfunction(mixin.stream),
    )

    assert result == (["self", "progress"], inspect.Parameter.KEYWORD_ONLY, None, is_async)


def test_stream_jsonl_name_is_gone():
    result = hasattr(StreamJSONLMixin, "stream_jsonl") or hasattr(
        AsyncStreamJSONLMixin, "stream_jsonl"
    )

    assert result is False
