import httpx
import pytest
import respx

from mpt_api_client import RQLQuery
from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import AsyncStreamJSONLMixin, StreamJSONLMixin
from tests.unit.conftest import API_URL, DummyModel

JSONL_BODY = b'{"id": "ID-1", "name": "Charge 1"}\n\n{"id": "ID-2", "name": "Charge 2"}\n'


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
async def test_async_stream_yields_models(async_stream_service):
    route = respx.get(f"{API_URL}/api/v1/charges").mock(
        return_value=httpx.Response(httpx.codes.OK, content=JSONL_BODY)
    )

    result = [charge async for charge in async_stream_service.stream()]

    request = route.calls[0].request
    assert [charge.id for charge in result] == ["ID-1", "ID-2"]
    assert all(isinstance(charge, DummyModel) for charge in result)
    assert request.headers["Accept"] == "application/jsonl"
