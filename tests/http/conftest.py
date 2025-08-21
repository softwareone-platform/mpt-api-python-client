import pytest

from mpt_api_client.http.client import HTTPClient
from mpt_api_client.http.collection import CollectionBaseClient
from mpt_api_client.http.resource import ResourceBaseClient
from mpt_api_client.models import Collection
from tests.conftest import DummyResource


class DummyResourceClient(ResourceBaseClient[DummyResource]):
    _endpoint = "/api/v1/test-resource"
    _resource_class = DummyResource


class DummyCollectionClient(CollectionBaseClient[DummyResource, DummyResourceClient]):
    _endpoint = "/api/v1/test"
    _resource_class = DummyResource
    _resource_client_class = DummyResourceClient
    _collection_class = Collection[DummyResource]


@pytest.fixture
def api_url():
    return "https://api.example.com"


@pytest.fixture
def api_token():
    return "test-token"


@pytest.fixture
def mpt_client(api_url, api_token):
    return HTTPClient(base_url=api_url, api_token=api_token)


@pytest.fixture
def resource_client(mpt_client):
    return DummyResourceClient(client=mpt_client, resource_id="RES-123")


@pytest.fixture
def collection_client(mpt_client) -> DummyCollectionClient:
    return DummyCollectionClient(client=mpt_client)
