import httpx
import pytest
import respx

from mpt_api_client import RQLQuery
from mpt_api_client.exceptions import (
    MPTHttpError,
    MPTStreamingError,
    MPTStreamingNotAcceptableError,
    MPTStreamingNotEnabledError,
    MPTStreamingNotSupportedError,
)
from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import AsyncStreamingMixin, StreamingMixin
from tests.unit.conftest import API_URL, DummyModel
from tests.unit.http.conftest import AsyncRecordingProgress, RecordingProgress

STREAM_URL = f"{API_URL}/api/v1/orders"
JSONL_BODY = b'{"id": "ID-1", "name": "Order 1"}\n\n{"id": "ID-2", "name": "Order 2"}\n'
NOT_CONFIRMED_MATCH = "did not confirm streaming mode"


class DummyStreamingService(
    StreamingMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/api/v1/orders"
    _model_class = DummyModel


class AsyncDummyStreamingService(
    AsyncStreamingMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/api/v1/orders"
    _model_class = DummyModel


@pytest.fixture
def streaming_service(http_client):
    return DummyStreamingService(http_client=http_client)


@pytest.fixture
def async_streaming_service(async_http_client):
    return AsyncDummyStreamingService(http_client=async_http_client)


def streaming_response():
    return jsonl_response({"MPT-Streaming": "true"})


def jsonl_response(headers=None):
    return httpx.Response(httpx.codes.OK, content=JSONL_BODY, headers=headers)


@respx.mock
def test_stream_sends_streaming_opt_in_headers(streaming_service):
    route = respx.get(STREAM_URL).mock(return_value=streaming_response())

    list(streaming_service.stream())  # act

    request = route.calls[0].request
    assert request.headers["MPT-Streaming"] == "true"
    assert request.headers["Accept"] == "application/jsonl"


@respx.mock
def test_stream_yields_models(streaming_service):
    respx.get(STREAM_URL).mock(return_value=streaming_response())

    result = list(streaming_service.stream())

    assert [order.id for order in result] == ["ID-1", "ID-2"]
    assert all(isinstance(order, DummyModel) for order in result)


@respx.mock
def test_stream_applies_query_filters(streaming_service):
    route = respx.get(STREAM_URL).mock(return_value=streaming_response())

    result = list(streaming_service.filter(RQLQuery(status="active")).stream())

    request = route.calls[0].request
    assert result
    assert "status" in request.url.query.decode()


@respx.mock
def test_stream_raises_when_not_confirmed(streaming_service):
    respx.get(STREAM_URL).mock(return_value=jsonl_response())
    iterator = streaming_service.stream()

    with pytest.raises(MPTStreamingNotEnabledError, match=NOT_CONFIRMED_MATCH):
        next(iterator)


@respx.mock
def test_stream_raises_on_false_header(streaming_service):
    respx.get(STREAM_URL).mock(return_value=jsonl_response({"MPT-Streaming": "false"}))
    iterator = streaming_service.stream()

    with pytest.raises(MPTStreamingNotEnabledError, match="got 'false'"):
        next(iterator)


@respx.mock
def test_stream_accepts_uppercase_value(streaming_service):
    respx.get(STREAM_URL).mock(return_value=jsonl_response({"MPT-Streaming": "True"}))

    result = list(streaming_service.stream())

    assert [order.id for order in result] == ["ID-1", "ID-2"]


@respx.mock
def test_stream_progress_events(streaming_service, recording_progress: RecordingProgress):
    respx.get(STREAM_URL).mock(return_value=streaming_response())

    list(streaming_service.stream(progress=recording_progress))  # act

    assert recording_progress.events == [
        ("item_processed",),
        ("item_processed",),
        ("completed",),
    ]


@respx.mock
async def test_async_stream_sends_opt_in_headers(async_streaming_service):
    route = respx.get(STREAM_URL).mock(return_value=streaming_response())

    [order async for order in async_streaming_service.stream()]  # act

    request = route.calls[0].request
    assert request.headers["MPT-Streaming"] == "true"
    assert request.headers["Accept"] == "application/jsonl"


@respx.mock
async def test_async_stream_yields_models(async_streaming_service):
    respx.get(STREAM_URL).mock(return_value=streaming_response())

    result = [order async for order in async_streaming_service.stream()]

    assert [order.id for order in result] == ["ID-1", "ID-2"]
    assert all(isinstance(order, DummyModel) for order in result)


@respx.mock
async def test_async_stream_raises_not_confirmed(async_streaming_service):
    respx.get(STREAM_URL).mock(return_value=jsonl_response())
    iterator = async_streaming_service.stream()

    with pytest.raises(MPTStreamingNotEnabledError, match=NOT_CONFIRMED_MATCH):
        await anext(iterator)


@respx.mock
async def test_async_stream_progress_events(
    async_streaming_service, async_recording_progress: AsyncRecordingProgress
):
    respx.get(STREAM_URL).mock(return_value=streaming_response())

    [order async for order in async_streaming_service.stream(progress=async_recording_progress)]

    assert async_recording_progress.events == [
        ("item_processed",),
        ("item_processed",),
        ("completed",),
    ]


@respx.mock
def test_stream_raises_when_not_implemented(streaming_service):
    respx.get(STREAM_URL).mock(return_value=httpx.Response(httpx.codes.NOT_IMPLEMENTED))
    iterator = streaming_service.stream()

    with pytest.raises(MPTStreamingNotSupportedError, match="does not support streaming mode"):
        next(iterator)


@respx.mock
def test_stream_raises_when_not_acceptable(streaming_service):
    respx.get(STREAM_URL).mock(return_value=httpx.Response(httpx.codes.NOT_ACCEPTABLE))
    iterator = streaming_service.stream()

    with pytest.raises(MPTStreamingNotAcceptableError, match="requested streaming format"):
        next(iterator)


@respx.mock
def test_streaming_errors_stay_catchable_as_http(streaming_service):
    respx.get(STREAM_URL).mock(return_value=httpx.Response(httpx.codes.NOT_IMPLEMENTED))
    iterator = streaming_service.stream()

    with pytest.raises(MPTHttpError) as raised:
        next(iterator)

    assert raised.value.status_code == httpx.codes.NOT_IMPLEMENTED
    assert isinstance(raised.value, MPTStreamingError)


@respx.mock
def test_other_http_errors_are_not_translated(streaming_service):
    respx.get(STREAM_URL).mock(return_value=httpx.Response(httpx.codes.FORBIDDEN))
    iterator = streaming_service.stream()

    with pytest.raises(MPTHttpError) as raised:
        next(iterator)

    assert raised.value.status_code == httpx.codes.FORBIDDEN
    assert not isinstance(raised.value, MPTStreamingError)


@respx.mock
def test_not_enabled_error_is_a_streaming_error(streaming_service):
    respx.get(STREAM_URL).mock(return_value=jsonl_response())
    iterator = streaming_service.stream()

    with pytest.raises(MPTStreamingError):
        next(iterator)


@respx.mock
async def test_async_stream_raises_not_supported(async_streaming_service):
    respx.get(STREAM_URL).mock(return_value=httpx.Response(httpx.codes.NOT_IMPLEMENTED))
    iterator = async_streaming_service.stream()

    with pytest.raises(MPTStreamingNotSupportedError):
        await anext(iterator)


@respx.mock
async def test_async_stream_raises_not_acceptable(async_streaming_service):
    respx.get(STREAM_URL).mock(return_value=httpx.Response(httpx.codes.NOT_ACCEPTABLE))
    iterator = async_streaming_service.stream()

    with pytest.raises(MPTStreamingNotAcceptableError):
        await anext(iterator)
