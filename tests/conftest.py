import pytest

from mpt_api_client.http.client import HTTPClient
from mpt_api_client.models import Resource

API_TOKEN = "test-token"
API_URL = "https://api.example.com"


class DummyResource(Resource):
    """Dummy resource for testing."""

    _data_key = "data"


@pytest.fixture
def mpt_client():
    return HTTPClient(base_url=API_URL, api_token=API_TOKEN)
