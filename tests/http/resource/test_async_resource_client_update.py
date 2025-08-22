import re

import httpx
import pytest
import respx


@pytest.mark.asyncio
async def test_update_success(async_resource_client):
    update_data = {"name": "Updated Resource", "status": "inactive"}
    expected_response = httpx.Response(
        httpx.codes.OK,
        json={"data": {"id": "RES-123", "name": "Updated Resource", "status": "inactive"}},
    )

    with respx.mock:
        mock_route = respx.put("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=expected_response
        )

        resource = await async_resource_client.update(update_data)

    assert resource.to_dict() == {"id": "RES-123", "name": "Updated Resource", "status": "inactive"}
    assert mock_route.called
    assert mock_route.call_count == 1


@pytest.mark.asyncio
async def test_save_success(async_resource_client):
    # First, set up the resource
    fetch_response = httpx.Response(
        httpx.codes.OK,
        json={"data": {"id": "RES-123", "name": "Original Name", "status": "active"}},
    )

    update_response = httpx.Response(
        httpx.codes.OK,
        json={"data": {"id": "RES-123", "name": "Modified Name", "status": "active"}},
    )

    with respx.mock:
        respx.get("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=fetch_response
        )
        mock_update_route = respx.put("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=update_response
        )

        await async_resource_client.fetch()
        async_resource_client.name = "Modified Name"
        resource = await async_resource_client.save()

    assert resource is async_resource_client
    assert async_resource_client.to_dict() == {
        "id": "RES-123",
        "name": "Modified Name",
        "status": "active",
    }
    assert (
        mock_update_route.calls[0].request.content
        == b'{"id":"RES-123","name":"Modified Name","status":"active"}'
    )
    assert mock_update_route.call_count == 1


@pytest.mark.asyncio
async def test_save_raises_error_when_resource_not_set(async_resource_client):
    expected_message = (
        "Resource data not available. Call fetch() method first to retrieve "
        "the resource `DummyResource`"
    )
    with pytest.raises(RuntimeError, match=re.escape(expected_message)):
        await async_resource_client.save()


@pytest.mark.asyncio
async def test_delete_success(async_resource_client):
    delete_response = httpx.Response(httpx.codes.NO_CONTENT)

    with respx.mock:
        mock_route = respx.delete("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=delete_response
        )

        await async_resource_client.delete()

    assert mock_route.called
    assert mock_route.call_count == 1
    assert async_resource_client.resource_ is None
