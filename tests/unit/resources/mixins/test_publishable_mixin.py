import httpx
import pytest
import respx

from mpt_api_client.http.async_service import AsyncService
from mpt_api_client.http.service import Service
from mpt_api_client.resources.mixins import (
    AsyncPublishableMixin,
    PublishableMixin,
)
from tests.unit.conftest import DummyModel


class DummyPublishableService(
    PublishableMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/publishable/"
    _model_class = DummyModel
    _collection_key = "data"


class DummyAsyncPublishableService(
    AsyncPublishableMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/publishable/"
    _model_class = DummyModel
    _collection_key = "data"


@pytest.fixture
def publishable_service(http_client):
    return DummyPublishableService(http_client=http_client)


@pytest.fixture
def async_publishable_service(async_http_client):
    return DummyAsyncPublishableService(http_client=async_http_client)


@pytest.mark.parametrize("action", ["publish", "unpublish"])
def test_actions_with_data(publishable_service, action):
    resource_data = {"id": "PRD-123", "status": "update"}
    response_expected_data = {"id": "PRD-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/publishable/PRD-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(publishable_service, action)("PRD-123", resource_data)

    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.content == b'{"id":"PRD-123","status":"update"}'
    assert result.to_dict() == response_expected_data
    assert isinstance(result, DummyModel)


@pytest.mark.parametrize("action", ["publish", "unpublish"])
def test_actions_no_data(publishable_service, action):
    response_expected_data = {"id": "PRD-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/publishable/PRD-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(publishable_service, action)("PRD-123")

    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.content == b""
    assert result.to_dict() == response_expected_data
    assert isinstance(result, DummyModel)


@pytest.mark.parametrize("action", ["publish", "unpublish"])
async def test_async_actions_with_data(async_publishable_service, action):
    resource_data = {"id": "PRD-123", "status": "update"}
    response_expected_data = {"id": "PRD-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/publishable/PRD-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_publishable_service, action)("PRD-123", resource_data)

    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.content == b'{"id":"PRD-123","status":"update"}'
    assert result.to_dict() == response_expected_data
    assert isinstance(result, DummyModel)


@pytest.mark.parametrize("action", ["publish", "unpublish"])
async def test_async_actions_no_data(async_publishable_service, action):
    response_expected_data = {"id": "PRD-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/publishable/PRD-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_publishable_service, action)("PRD-123")

    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.content == b""
    assert result.to_dict() == response_expected_data
    assert isinstance(result, DummyModel)
