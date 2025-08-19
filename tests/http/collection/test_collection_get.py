def test_get(collection_client):
    resource = collection_client.get("RES-123")
    assert resource.resource_id_ == "RES-123"
    assert isinstance(resource, collection_client._resource_client_class)  # noqa: SLF001
