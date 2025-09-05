import json

import httpx
import respx


async def test_async_create_mixin(async_dummy_service):  # noqa: WPS210
    resource_data = {"name": "Test Resource", "status": "active"}
    new_resource_data = {"id": "new-resource-id", "name": "Test Resource", "status": "active"}
    create_response = httpx.Response(httpx.codes.OK, json=new_resource_data)

    with respx.mock:
        mock_route = respx.post("https://api.example.com/api/v1/test").mock(
            return_value=create_response
        )

        created_resource = await async_dummy_service.create(resource_data)

    assert created_resource.to_dict() == new_resource_data
    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "POST"
    assert request.url == "https://api.example.com/api/v1/test"
    assert json.loads(request.content.decode()) == resource_data


async def test_async_delete_mixin(async_dummy_service):  # noqa: WPS210
    delete_response = httpx.Response(httpx.codes.NO_CONTENT, json=None)

    with respx.mock:
        mock_route = respx.delete("https://api.example.com/api/v1/test/RES-123").mock(
            return_value=delete_response
        )

        await async_dummy_service.delete("RES-123")

    assert mock_route.call_count == 1


async def test_async_update_resource(async_dummy_service):  # noqa: WPS210
    resource_data = {"name": "Test Resource", "status": "active"}
    update_response = httpx.Response(httpx.codes.OK, json=resource_data)

    with respx.mock:
        mock_route = respx.put("https://api.example.com/api/v1/test/RES-123").mock(
            return_value=update_response
        )

        await async_dummy_service.update("RES-123", resource_data)

    request: httpx.Request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert json.loads(request.content.decode()) == resource_data


def test_sync_create_mixin(dummy_service):  # noqa: WPS210
    resource_data = {"name": "Test Resource", "status": "active"}
    new_resource_data = {"id": "new-resource-id", "name": "Test Resource", "status": "active"}
    create_response = httpx.Response(httpx.codes.OK, json=new_resource_data)

    with respx.mock:
        mock_route = respx.post("https://api.example.com/api/v1/test").mock(
            return_value=create_response
        )

        created_resource = dummy_service.create(resource_data)

    assert created_resource.to_dict() == new_resource_data
    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "POST"
    assert request.url == "https://api.example.com/api/v1/test"
    assert json.loads(request.content.decode()) == resource_data


def test_sync_delete_mixin(dummy_service):
    delete_response = httpx.Response(httpx.codes.NO_CONTENT, json=None)
    with respx.mock:
        mock_route = respx.delete("https://api.example.com/api/v1/test/RES-123").mock(
            return_value=delete_response
        )

        dummy_service.delete("RES-123")

    assert mock_route.call_count == 1


def test_sync_update_resource(dummy_service):
    resource_data = {"name": "Test Resource", "status": "active"}
    update_response = httpx.Response(httpx.codes.OK, json=resource_data)
    with respx.mock:
        mock_route = respx.put("https://api.example.com/api/v1/test/RES-123").mock(
            return_value=update_response
        )

        dummy_service.update("RES-123", resource_data)

    request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert json.loads(request.content.decode()) == resource_data
