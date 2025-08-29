import pytest

from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.models import Model

API_TOKEN = "test-token"
API_URL = "https://api.example.com"


class DummyModel(Model):
    """Dummy resource for testing."""

    _data_key = None


@pytest.fixture
def http_client():
    return HTTPClient(base_url=API_URL, api_token=API_TOKEN)


@pytest.fixture
def async_http_client():
    return AsyncHTTPClient(base_url=API_URL, api_token=API_TOKEN)
