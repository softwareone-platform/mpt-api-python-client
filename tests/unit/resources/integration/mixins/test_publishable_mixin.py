import httpx
import pytest
import respx

from mpt_api_client.http.async_service import AsyncService
from mpt_api_client.http.service import Service
from mpt_api_client.resources.integration.mixins import (
    AsyncPublishableMixin,
    PublishableMixin,
)
from tests.unit.conftest import DummyModel


class DummyPublishableService(
    PublishableMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/integration/extensions/EXT-001/terms"
    _model_class = DummyModel
    _collection_key = "data"


class DummyAsyncPublishableService(
    AsyncPublishableMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/integration/extensions/EXT-001/terms"
    _model_class = DummyModel
    _collection_key = "data"


@pytest.fixture
def publishable_service(http_client):
    return DummyPublishableService(http_client=http_client)


@pytest.fixture
def async_publishable_service(async_http_client):
    return DummyAsyncPublishableService(http_client=async_http_client)


@pytest.mark.parametrize("action", ["publish", "unpublish"])
def test_action_with_data(publishable_service, action):
    resource_data = {"id": "TERM-001", "status": "update"}
    expected_response = {"id": "TERM-001", "status": "Published"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/integration/extensions/EXT-001/terms/TERM-001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=expected_response,
            )
        )

        result = getattr(publishable_service, action)("TERM-001", resource_data)

    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "POST"
    assert request.content == b'{"id":"TERM-001","status":"update"}'
    assert result.to_dict() == expected_response
    assert isinstance(result, DummyModel)


@pytest.mark.parametrize("action", ["publish", "unpublish"])
def test_action_no_data(publishable_service, action):
    expected_response = {"id": "TERM-001", "status": "Published"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/integration/extensions/EXT-001/terms/TERM-001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=expected_response,
            )
        )

        result = getattr(publishable_service, action)("TERM-001")

    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "POST"
    assert request.content == b""
    assert result.to_dict() == expected_response
    assert isinstance(result, DummyModel)


@pytest.mark.parametrize("action", ["publish", "unpublish"])
async def test_async_action_with_data(async_publishable_service, action):
    resource_data = {"id": "TERM-001", "status": "update"}
    expected_response = {"id": "TERM-001", "status": "Published"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/integration/extensions/EXT-001/terms/TERM-001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=expected_response,
            )
        )

        result = await getattr(async_publishable_service, action)("TERM-001", resource_data)

    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "POST"
    assert request.content == b'{"id":"TERM-001","status":"update"}'
    assert result.to_dict() == expected_response
    assert isinstance(result, DummyModel)


@pytest.mark.parametrize("action", ["publish", "unpublish"])
async def test_async_action_no_data(async_publishable_service, action):
    expected_response = {"id": "TERM-001", "status": "Published"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/integration/extensions/EXT-001/terms/TERM-001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=expected_response,
            )
        )

        result = await getattr(async_publishable_service, action)("TERM-001")

    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "POST"
    assert request.content == b""
    assert result.to_dict() == expected_response
    assert isinstance(result, DummyModel)
