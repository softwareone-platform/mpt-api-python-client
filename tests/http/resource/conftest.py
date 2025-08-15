import pytest

from mpt_api_client.http.client import MPTClient
from mpt_api_client.http.resource import ResourceBaseClient
from tests.http.conftest import DummyResource


class DummyResourceClient(ResourceBaseClient[DummyResource]):
    _endpoint = "/api/v1/test-resource"
    _resource_class = DummyResource


@pytest.fixture
def api_url():
    return "https://api.example.com"


@pytest.fixture
def api_token():
    return "test-token"


@pytest.fixture
def mpt_client(api_url, api_token):
    return MPTClient(base_url=api_url, api_token=api_token)


@pytest.fixture
def resource_client(mpt_client):
    return DummyResourceClient(client=mpt_client, resource_id="RES-123")
