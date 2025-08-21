import pytest
import respx
from httpx import ConnectTimeout, Response, codes

from mpt_api_client.http.client import HTTPClientAsync
from tests.conftest import API_TOKEN, API_URL


def test_mpt_client_initialization():
    client = HTTPClientAsync(base_url=API_URL, api_token=API_TOKEN)

    assert client.base_url == API_URL
    assert client.headers["Authorization"] == "Bearer test-token"
    assert client.headers["User-Agent"] == "swo-marketplace-client/1.0"


def test_env_initialization(monkeypatch):
    monkeypatch.setenv("MPT_TOKEN", API_TOKEN)
    monkeypatch.setenv("MPT_URL", API_URL)

    client = HTTPClientAsync()

    assert client.base_url == API_URL
    assert client.headers["Authorization"] == f"Bearer {API_TOKEN}"


def test_mpt_client_without_token():
    with pytest.raises(ValueError):
        HTTPClientAsync(base_url=API_URL)


def test_mpt_client_without_url():
    with pytest.raises(ValueError):
        HTTPClientAsync(api_token=API_TOKEN)


@respx.mock
async def test_mock_call_success(http_client_async):
    success_route = respx.get(f"{API_URL}/").mock(
        return_value=Response(200, json={"message": "Hello, World!"})
    )

    success_response = await http_client_async.get("/")

    assert success_response.status_code == codes.OK
    assert success_response.json() == {"message": "Hello, World!"}
    assert success_route.called


@respx.mock
async def test_mock_call_failure(http_client_async):
    timeout_route = respx.get(f"{API_URL}/timeout").mock(side_effect=ConnectTimeout("Mock Timeout"))

    with pytest.raises(ConnectTimeout):
        await http_client_async.get("/timeout")

    assert timeout_route.called
