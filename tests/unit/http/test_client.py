import json

import pytest
import respx
from httpx import ConnectTimeout, Response, codes

from mpt_api_client.exceptions import MPTError
from mpt_api_client.http.client import HTTPClient
from tests.unit.conftest import API_TOKEN, API_URL


def test_http_initialization(mocker):
    mock_client = mocker.patch("mpt_api_client.http.client.Client")

    HTTPClient(base_url=API_URL, api_token=API_TOKEN)

    mock_client.assert_called_once_with(
        base_url=API_URL,
        headers={
            "User-Agent": "swo-marketplace-client/1.0",
            "Authorization": "Bearer test-token",
        },
        timeout=5.0,
        transport=mocker.ANY,
    )


def test_env_initialization(monkeypatch, mocker):
    monkeypatch.setenv("MPT_TOKEN", API_TOKEN)
    monkeypatch.setenv("MPT_URL", API_URL)
    mock_client = mocker.patch("mpt_api_client.http.client.Client")

    HTTPClient()

    mock_client.assert_called_once_with(
        base_url=API_URL,
        headers={
            "User-Agent": "swo-marketplace-client/1.0",
            "Authorization": f"Bearer {API_TOKEN}",
        },
        timeout=5.0,
        transport=mocker.ANY,
    )


def test_http_without_token():
    with pytest.raises(ValueError):
        HTTPClient(base_url=API_URL)


def test_http_without_url():
    with pytest.raises(ValueError):
        HTTPClient(api_token=API_TOKEN)


@respx.mock
def test_http_call_success(http_client):
    success_route = respx.get(f"{API_URL}/").mock(
        return_value=Response(200, json={"message": "Hello, World!"})
    )

    success_response = http_client.request("GET", "/")

    assert success_response.status_code == codes.OK
    assert json.loads(success_response.content) == {"message": "Hello, World!"}
    assert success_route.called


@respx.mock
def test_http_call_failure(http_client):
    timeout_route = respx.get(f"{API_URL}/timeout").mock(side_effect=ConnectTimeout("Mock Timeout"))

    with pytest.raises(MPTError, match="HTTP Error: Mock Timeout"):
        http_client.request("GET", "/timeout")

    assert timeout_route.called
