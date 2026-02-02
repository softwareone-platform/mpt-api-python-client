import json

import httpx
import respx

from tests.unit.http.conftest import AsyncDummyService, DummyService


async def test_async_update_resource(async_dummy_service: AsyncDummyService) -> None:
    """Test updating a resource asynchronously."""
    resource_data = {"name": "Test Resource", "status": "active"}
    update_response = httpx.Response(httpx.codes.OK, json=resource_data)
    with respx.mock:
        mock_route = respx.put("https://api.example.com/api/v1/test/RES-123").mock(
            return_value=update_response
        )

        await async_dummy_service.update("RES-123", resource_data)  # act

    request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert json.loads(request.content.decode()) == resource_data


def test_sync_update_resource(dummy_service: DummyService) -> None:
    """Test updating a resource synchronously."""
    resource_data = {"name": "Test Resource", "status": "active"}
    update_response = httpx.Response(httpx.codes.OK, json=resource_data)
    with respx.mock:
        mock_route = respx.put("https://api.example.com/api/v1/test/RES-123").mock(
            return_value=update_response
        )

        dummy_service.update("RES-123", resource_data)  # act

    request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert json.loads(request.content.decode()) == resource_data
