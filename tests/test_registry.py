import pytest

from mpt_api_client.http.collection import CollectionClientBase
from mpt_api_client.http.resource import ResourceBaseClient
from mpt_api_client.models import Resource
from mpt_api_client.registry import Registry


class DummyResource(Resource):
    """Dummy resource for testing."""


class DummyCollectionClientBase(CollectionClientBase):
    _endpoint = "/api/v1/dummy"
    _resource_class = DummyResource


def test_register_collection_client_successfully():
    registry = Registry()
    keyname = "test_collection"

    registry.register(keyname, DummyCollectionClientBase)

    assert keyname in registry.items
    assert registry.items[keyname] == DummyCollectionClientBase
    assert registry.get(keyname) == DummyCollectionClientBase


def test_get_registered_client_successfully():
    registry = Registry()
    keyname = "orders"

    registry.register(keyname, DummyCollectionClientBase)

    retrieved_client = registry.get(keyname)

    assert retrieved_client == DummyCollectionClientBase


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
        registry.register(keyname, DummyCollectionClientBase)

    registry_keys = registry.list_keys()

    assert sorted(registry_keys) == sorted(expected_keys)
    assert len(registry_keys) == 3


def test_registry_as_decorator():
    registry = Registry()

    @registry("test_call")
    class TestCallClientBase(  # noqa: WPS431
        CollectionClientBase[DummyResource, ResourceBaseClient[DummyResource]]
    ):
        _endpoint = "/api/v1/test-call"
        _resource_class = DummyResource

    registered_client = registry.get("test_call")

    assert registered_client == TestCallClientBase
