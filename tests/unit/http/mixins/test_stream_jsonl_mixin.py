import httpx
import pytest
import respx

from mpt_api_client import RQLQuery
from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import AsyncStreamJSONLMixin, StreamJSONLMixin
from tests.unit.conftest import API_URL, DummyModel
from tests.unit.http.conftest import AsyncRecordingProgress, RecordingProgress

JSONL_BODY = b'{"id": "ID-1", "name": "Charge 1"}\n\n{"id": "ID-2", "name": "Charge 2"}\n'
MALFORMED_JSONL_BODY = b'not-json\n{"id": "ID-1", "name": "Charge 1"}\n'


class DummyStreamService(  # noqa: WPS215
    StreamJSONLMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/api/v1/charges"
    _model_class = DummyModel


class AsyncDummyStreamService(  # noqa: WPS215
    AsyncStreamJSONLMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/api/v1/charges"
    _model_class = DummyModel


@pytest.fixture
def stream_service(http_client):
    return DummyStreamService(http_client=http_client)


@pytest.fixture
def async_stream_service(async_http_client):
    return AsyncDummyStreamService(http_client=async_http_client)


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
def test_stream_progress_malformed_line(stream_service, recording_progress: RecordingProgress):
    respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=MALFORMED_JSONL_BODY)
    )
    iterator = stream_service.stream(progress=recording_progress)

    with pytest.raises(ValueError, match="Expecting value"):
        next(iterator)

    assert recording_progress.events == []


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
async def test_async_stream_progress_malformed_line(
    async_stream_service, async_recording_progress: AsyncRecordingProgress
):
    respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=MALFORMED_JSONL_BODY)
    )
    iterator = async_stream_service.stream(progress=async_recording_progress)

    with pytest.raises(ValueError, match="Expecting value"):
        await anext(iterator)

    assert async_recording_progress.events == []
