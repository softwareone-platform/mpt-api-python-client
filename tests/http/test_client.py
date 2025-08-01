import pytest
import respx
from httpx import ConnectTimeout, Response, codes

from mpt_api_client.http.client import MPTClient

API_TOKEN = "test-token"
API_URL = "https://api.example.com"


@pytest.fixture
def mpt_client():
    return MPTClient(base_url=API_URL, api_token=API_TOKEN)


def test_mpt_client_initialization():
    client = MPTClient(base_url=API_URL, api_token=API_TOKEN)

    assert client.api_token == API_TOKEN
    assert client.base_url == API_URL
    assert client.headers["Authorization"] == "Bearer test-token"
    assert client.headers["User-Agent"] == "swo-marketplace-client/1.0"


@respx.mock
def test_mock_call_success(mpt_client):
    success_route = respx.get(f"{API_URL}/").mock(
        return_value=Response(200, json={"message": "Hello, World!"})
    )

    success_response = mpt_client.get("/")

    assert success_response.status_code == codes.OK
    assert success_response.json() == {"message": "Hello, World!"}
    assert success_route.called


@respx.mock
def test_mock_call_failure(mpt_client):
    timeout_route = respx.get(f"{API_URL}/timeout").mock(side_effect=ConnectTimeout("Mock Timeout"))

    with pytest.raises(ConnectTimeout):
        mpt_client.get("/timeout")

    assert timeout_route.called


@respx.mock
def test_mock_call_failure_with_retries(mpt_client):
    not_found_route = respx.get(f"{API_URL}/not-found").mock(
        side_effect=Response(codes.NOT_FOUND, json={"message": "Not Found"})
    )

    not_found_response = mpt_client.get("/not-found")

    assert not_found_response.status_code == codes.NOT_FOUND
    assert not_found_route.called
