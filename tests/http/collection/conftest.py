import pytest

from mpt_api_client.http.collection import CollectionBaseClient
from mpt_api_client.models import Collection, Resource


class DummyResource(Resource):
    """Dummy resource for testing."""


class DummyCollectionClient(CollectionBaseClient[DummyResource]):
    _endpoint = "/api/v1/test"
    _resource_class = DummyResource
    _collection_class = Collection[DummyResource]


@pytest.fixture
def collection_client(mpt_client):
    return DummyCollectionClient(client=mpt_client)
