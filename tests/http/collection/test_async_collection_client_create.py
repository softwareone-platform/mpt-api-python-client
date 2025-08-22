import json

import httpx
import pytest
import respx


@pytest.mark.asyncio
async def test_create_resource(async_collection_client):  # noqa: WPS210
    resource_data = {"name": "Test Resource", "status": "active"}
    new_resource_data = {"id": "new-resource-id", "name": "Test Resource", "status": "active"}
    create_response = httpx.Response(201, json={"data": new_resource_data})

    with respx.mock:
        mock_route = respx.post("https://api.example.com/api/v1/test").mock(
            return_value=create_response
        )

        created_resource = await async_collection_client.create(resource_data)

    assert created_resource.to_dict() == new_resource_data
    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "POST"
    assert request.url == "https://api.example.com/api/v1/test"
    assert json.loads(request.content.decode()) == resource_data
