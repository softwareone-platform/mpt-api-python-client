import pytest

from mpt_api_client.http.client import HTTPClient, HTTPClientAsync
from mpt_api_client.http.collection import CollectionClientBase
from mpt_api_client.http.resource import ResourceBaseClient
from mpt_api_client.models import Collection
from tests.conftest import DummyResource


class DummyResourceClient(ResourceBaseClient[DummyResource]):
    _endpoint = "/api/v1/test-resource"
    _resource_class = DummyResource


class DummyCollectionClientBase(CollectionClientBase[DummyResource, DummyResourceClient]):
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
def http_client(api_url, api_token):
    return HTTPClient(base_url=api_url, api_token=api_token)


@pytest.fixture
def http_client_async(api_url, api_token):
    return HTTPClientAsync(base_url=api_url, api_token=api_token)


@pytest.fixture
def resource_client(http_client):
    return DummyResourceClient(http_client=http_client, resource_id="RES-123")


@pytest.fixture
def collection_client(http_client) -> DummyCollectionClientBase:
    return DummyCollectionClientBase(http_client=http_client)
