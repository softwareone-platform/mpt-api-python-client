import pytest
import respx
from httpx import ConnectTimeout, Response, codes

from mpt_api_client.exceptions import MPTError
from mpt_api_client.http.async_client import AsyncHTTPClient
from tests.conftest import API_TOKEN, API_URL


def test_async_http_initialization():
    client = AsyncHTTPClient(base_url=API_URL, api_token=API_TOKEN)

    assert client.base_url == API_URL
    assert client.headers["Authorization"] == "Bearer test-token"
    assert client.headers["User-Agent"] == "swo-marketplace-client/1.0"


def test_async_http_env_initialization(monkeypatch):
    monkeypatch.setenv("MPT_TOKEN", API_TOKEN)
    monkeypatch.setenv("MPT_URL", API_URL)

    client = AsyncHTTPClient()

    assert client.base_url == API_URL
    assert client.headers["Authorization"] == f"Bearer {API_TOKEN}"


def test_async_http_without_token():
    with pytest.raises(ValueError):
        AsyncHTTPClient(base_url=API_URL)


def test_async_http_without_url():
    with pytest.raises(ValueError):
        AsyncHTTPClient(api_token=API_TOKEN)


@respx.mock
async def test_async_http_call_success(async_http_client):
    success_route = respx.get(f"{API_URL}/").mock(
        return_value=Response(200, json={"message": "Hello, World!"})
    )

    success_response = await async_http_client.get("/")

    assert success_response.status_code == codes.OK
    assert success_response.json() == {"message": "Hello, World!"}
    assert success_route.called


@respx.mock
async def test_async_http_call_failure(async_http_client):
    timeout_route = respx.get(f"{API_URL}/timeout").mock(side_effect=ConnectTimeout("Mock Timeout"))

    with pytest.raises(MPTError, match="HTTP Error: Mock Timeout"):
        await async_http_client.get("/timeout")

    assert timeout_route.called
