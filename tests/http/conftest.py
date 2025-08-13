import pytest

from mpt_api_client.http.client import MPTClient

API_TOKEN = "test-token"
API_URL = "https://api.example.com"


@pytest.fixture
def mpt_client():
    return MPTClient(base_url=API_URL, api_token=API_TOKEN)
