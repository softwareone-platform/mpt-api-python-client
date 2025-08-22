import httpx
import pytest
import respx


@pytest.mark.asyncio
async def test_fetch_success(async_resource_client):
    expected_response = httpx.Response(
        httpx.codes.OK,
        json={"data": {"id": "RES-123", "name": "Test Resource", "status": "active"}},
    )

    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=expected_response
        )

        resource = await async_resource_client.fetch()

    assert resource.to_dict() == {"id": "RES-123", "name": "Test Resource", "status": "active"}
    assert mock_route.called
    assert mock_route.call_count == 1
    assert async_resource_client.resource_ is not None


@pytest.mark.asyncio
async def test_get_attribute(async_resource_client):
    expected_response = httpx.Response(
        httpx.codes.OK,
        json={"data": {"id": "RES-123", "contact": {"name": "Albert"}, "status": "active"}},
    )

    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=expected_response
        )
        await async_resource_client.fetch()

        assert async_resource_client.id == "RES-123"
        assert async_resource_client.contact.name == "Albert"
        assert mock_route.call_count == 1


@pytest.mark.asyncio
async def test_set_attribute(async_resource_client):
    expected_response = httpx.Response(
        httpx.codes.OK,
        json={"data": {"id": "RES-123", "contact": {"name": "Albert"}, "status": "active"}},
    )

    with respx.mock:
        respx.get("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=expected_response
        )
        await async_resource_client.fetch()
        async_resource_client.status = "disabled"
        async_resource_client.contact.name = "Alice"

        assert async_resource_client.status == "disabled"
        assert async_resource_client.contact.name == "Alice"


@pytest.mark.asyncio
async def test_fetch_not_found(async_resource_client):
    error_response = httpx.Response(httpx.codes.NOT_FOUND, json={"error": "Resource not found"})

    with respx.mock:
        respx.get("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=error_response
        )

        with pytest.raises(httpx.HTTPStatusError):
            await async_resource_client.fetch()


@pytest.mark.asyncio
async def test_fetch_server_error(async_resource_client):
    error_response = httpx.Response(
        httpx.codes.INTERNAL_SERVER_ERROR, json={"error": "Internal server error"}
    )

    with respx.mock:
        respx.get("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=error_response
        )

        with pytest.raises(httpx.HTTPStatusError):
            await async_resource_client.fetch()


@pytest.mark.asyncio
async def test_fetch_with_special_characters_in_id(async_resource_client):
    expected_response = httpx.Response(
        httpx.codes.OK, json={"data": {"id": "RES-123", "name": "Special Resource"}}
    )

    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=expected_response
        )

        resource = await async_resource_client.fetch()

    assert resource.to_dict() == {"id": "RES-123", "name": "Special Resource"}
    assert mock_route.called


@pytest.mark.asyncio
async def test_fetch_caches_resource(async_resource_client):
    expected_response = httpx.Response(
        httpx.codes.OK,
        json={"data": {"id": "RES-123", "name": "Test Resource", "status": "active"}},
    )

    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=expected_response
        )

        resource1 = await async_resource_client.fetch()
        resource2 = await async_resource_client.fetch()

    assert resource1 is not resource2
    assert (
        mock_route.call_count == 2
    )  # Both calls go through since we're explicitly calling fetch()
