import json

import httpx
import pytest
import respx

from mpt_api_client import RQLQuery
from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import AsyncStreamJSONLMixin, StreamJSONLMixin
from tests.unit.conftest import API_URL, DummyModel
from tests.unit.http.conftest import (
    JSON_LEGAL_SEPARATORS,
    NON_OBJECT_LINE_CASES,
    AsyncRecordingProgress,
    RecordingProgress,
)

JSONL_BODY = b'{"id": "ID-1", "name": "Charge 1"}\n\n{"id": "ID-2", "name": "Charge 2"}\n'
MALFORMED_JSONL_BODY = b'not-json\n{"id": "ID-1", "name": "Charge 1"}\n'


def separator_jsonl_response(separator):
    body = f'{{"id": "ID-1", "name": "a{separator}b"}}\n'.encode()
    return httpx.Response(httpx.codes.OK, content=body)


def raw_line_response(line):
    return httpx.Response(httpx.codes.OK, content=f"{line}\n".encode())


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
def test_stream_jsonl_yields_models(stream_service):
    route = respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=JSONL_BODY)
    )

    result = list(stream_service.stream_jsonl())

    request = route.calls[0].request
    assert [charge.id for charge in result] == ["ID-1", "ID-2"]
    assert all(isinstance(charge, DummyModel) for charge in result)
    assert request.headers["Accept"] == "application/jsonl"


@pytest.mark.parametrize("separator", JSON_LEGAL_SEPARATORS)
@respx.mock
def test_stream_jsonl_keeps_json_legal_separator(stream_service, separator):
    expected_pair = ("ID-1", f"a{separator}b")
    respx.get(f"{API_URL}/api/v1/charges").mock(return_value=separator_jsonl_response(separator))

    result = list(stream_service.stream_jsonl())

    assert [(charge.id, charge.name) for charge in result] == [expected_pair]


@respx.mock
def test_stream_jsonl_applies_query_filters(stream_service):
    route = respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=JSONL_BODY)
    )

    result = list(stream_service.filter(RQLQuery(status="active")).stream_jsonl())

    request = route.calls[0].request
    assert result
    assert "status" in request.url.query.decode()


@respx.mock
def test_stream_jsonl_progress_events(stream_service, recording_progress: RecordingProgress):
    respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=JSONL_BODY)
    )

    list(stream_service.stream_jsonl(progress=recording_progress))  # act

    assert recording_progress.events == [
        ("item_processed",),
        ("item_processed",),
        ("completed",),
    ]


@respx.mock
def test_stream_jsonl_progress_early_break(stream_service, recording_progress: RecordingProgress):
    respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=JSONL_BODY)
    )
    iterator = stream_service.stream_jsonl(progress=recording_progress)
    next(iterator)

    iterator.close()  # act

    assert recording_progress.events == [("item_processed",)]


@respx.mock
def test_stream_jsonl_progress_bad_line(stream_service, recording_progress: RecordingProgress):
    respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=MALFORMED_JSONL_BODY)
    )
    iterator = stream_service.stream_jsonl(progress=recording_progress)

    with pytest.raises(ValueError, match="Expecting value"):
        next(iterator)

    assert recording_progress.events == []


@pytest.mark.parametrize("line", NON_OBJECT_LINE_CASES)
@respx.mock
def test_stream_jsonl_rejects_non_object_line(stream_service, line):
    respx.get(f"{API_URL}/api/v1/charges").mock(return_value=raw_line_response(line))
    iterator = stream_service.stream_jsonl()

    with pytest.raises(json.JSONDecodeError, match="record must be an object"):
        next(iterator)


@respx.mock
async def test_async_stream_jsonl_yields_models(async_stream_service):
    route = respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=JSONL_BODY)
    )

    result = [charge async for charge in async_stream_service.stream_jsonl()]

    request = route.calls[0].request
    assert [charge.id for charge in result] == ["ID-1", "ID-2"]
    assert all(isinstance(charge, DummyModel) for charge in result)
    assert request.headers["Accept"] == "application/jsonl"


@pytest.mark.parametrize("separator", JSON_LEGAL_SEPARATORS)
@respx.mock
async def test_async_stream_jsonl_keeps_separator(async_stream_service, separator):
    expected_pair = ("ID-1", f"a{separator}b")
    respx.get(f"{API_URL}/api/v1/charges").mock(return_value=separator_jsonl_response(separator))

    result = [charge async for charge in async_stream_service.stream_jsonl()]

    assert [(charge.id, charge.name) for charge in result] == [expected_pair]


@respx.mock
async def test_async_stream_jsonl_progress_events(
    async_stream_service, async_recording_progress: AsyncRecordingProgress
):
    respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=JSONL_BODY)
    )

    [
        charge
        async for charge in async_stream_service.stream_jsonl(progress=async_recording_progress)
    ]

    assert async_recording_progress.events == [
        ("item_processed",),
        ("item_processed",),
        ("completed",),
    ]


@respx.mock
async def test_async_stream_jsonl_progress_early_break(
    async_stream_service, async_recording_progress: AsyncRecordingProgress
):
    respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=JSONL_BODY)
    )
    iterator = async_stream_service.stream_jsonl(progress=async_recording_progress)

    await anext(iterator)
    await iterator.aclose()

    assert async_recording_progress.events == [("item_processed",)]


@respx.mock
async def test_async_stream_jsonl_progress_bad_line(
    async_stream_service, async_recording_progress: AsyncRecordingProgress
):
    respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=MALFORMED_JSONL_BODY)
    )
    iterator = async_stream_service.stream_jsonl(progress=async_recording_progress)

    with pytest.raises(ValueError, match="Expecting value"):
        await anext(iterator)

    assert async_recording_progress.events == []


@pytest.mark.parametrize("line", NON_OBJECT_LINE_CASES)
@respx.mock
async def test_async_stream_jsonl_rejects_non_object(async_stream_service, line):
    respx.get(f"{API_URL}/api/v1/charges").mock(return_value=raw_line_response(line))
    iterator = async_stream_service.stream_jsonl()

    with pytest.raises(json.JSONDecodeError, match="record must be an object"):
        await anext(iterator)
