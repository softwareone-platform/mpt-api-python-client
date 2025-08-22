import pytest


@pytest.mark.asyncio
async def test_get(async_collection_client):
    resource = await async_collection_client.get("RES-123")
    assert resource.resource_id_ == "RES-123"
    assert isinstance(resource, async_collection_client._resource_client_class)  # noqa: SLF001
