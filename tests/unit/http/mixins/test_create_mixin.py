import json

import httpx
import respx

from tests.unit.http.conftest import AsyncDummyService, DummyService


async def test_async_create_mixin(async_dummy_service: AsyncDummyService) -> None:
    """Test creating a resource asynchronously."""
    resource_data = {"name": "Test Resource", "status": "active"}
    new_resource_data = {"id": "new-resource-id", "name": "Test Resource", "status": "active"}
    create_response = httpx.Response(httpx.codes.OK, json=new_resource_data)
    with respx.mock:
        mock_route = respx.post("https://api.example.com/api/v1/test").mock(
            return_value=create_response
        )

        result = await async_dummy_service.create(resource_data)

    assert result.to_dict() == new_resource_data
    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "POST"
    assert request.url == "https://api.example.com/api/v1/test"
    assert json.loads(request.content.decode()) == resource_data


def test_sync_create_mixin(dummy_service: DummyService) -> None:
    """Test creating a resource synchronously."""
    resource_data = {"name": "Test Resource", "status": "active"}
    new_resource_data = {"id": "new-resource-id", "name": "Test Resource", "status": "active"}
    create_response = httpx.Response(httpx.codes.OK, json=new_resource_data)
    with respx.mock:
        mock_route = respx.post("https://api.example.com/api/v1/test").mock(
            return_value=create_response
        )

        result = dummy_service.create(resource_data)

    assert result.to_dict() == new_resource_data
    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "POST"
    assert request.url == "https://api.example.com/api/v1/test"
    assert json.loads(request.content.decode()) == resource_data
