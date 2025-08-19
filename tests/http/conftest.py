import pytest

from mpt_api_client.http.client import MPTClient
from mpt_api_client.models import Resource

API_TOKEN = "test-token"
API_URL = "https://api.example.com"


class DummyResource(Resource):
    """Dummy resource for testing."""


@pytest.fixture
def mpt_client():
    return MPTClient(base_url=API_URL, api_token=API_TOKEN)
