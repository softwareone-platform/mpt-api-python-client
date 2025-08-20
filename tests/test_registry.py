import pytest

from mpt_api_client.http.collection import CollectionBaseClient
from mpt_api_client.models import Resource
from mpt_api_client.registry import Registry


class DummyResource(Resource):
    """Dummy resource for testing."""


class DummyCollectionClient(CollectionBaseClient):
    _endpoint = "/api/v1/dummy"
    _resource_class = DummyResource


def test_register_collection_client_successfully():
    registry = Registry()
    keyname = "test_collection"

    registry.register(keyname, DummyCollectionClient)

    assert keyname in registry.items
    assert registry.items[keyname] == DummyCollectionClient
    assert registry.get(keyname) == DummyCollectionClient


def test_get_registered_client_successfully():
    registry = Registry()
    keyname = "orders"

    registry.register(keyname, DummyCollectionClient)

    retrieved_client = registry.get(keyname)

    assert retrieved_client == DummyCollectionClient


def test_get_raise_exception():
    registry = Registry()
    unregistered_keyname = "nonexistent_client"

    with pytest.raises(
        KeyError, match="No collection client registered with keyname: nonexistent_client"
    ):
        registry.get(unregistered_keyname)


def test_list_keys():
    registry = Registry()
    expected_keys = ["orders", "customers", "products"]

    for keyname in expected_keys:
        registry.register(keyname, DummyCollectionClient)

    registry_keys = registry.list_keys()

    assert sorted(registry_keys) == sorted(expected_keys)
    assert len(registry_keys) == 3


def test_registry_as_decorator():
    registry = Registry()

    @registry("test_call")
    class TestCallClient(CollectionBaseClient[DummyResource]):  # noqa: WPS431
        _endpoint = "/api/v1/test-call"
        _resource_class = DummyResource

    registered_client = registry.get("test_call")

    assert registered_client == TestCallClient
