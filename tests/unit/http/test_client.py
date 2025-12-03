import io
import json

import pytest
import respx
from httpx import ConnectTimeout, Response, codes

from mpt_api_client.exceptions import MPTError
from mpt_api_client.http.client import HTTPClient
from tests.unit.conftest import API_TOKEN, API_URL


def test_http_initialization(mocker):
    mock_client = mocker.patch("mpt_api_client.http.client.Client")

    HTTPClient(base_url=API_URL, api_token=API_TOKEN)  # act

    mock_client.assert_called_once_with(
        base_url=API_URL,
        follow_redirects=True,
        headers={
            "User-Agent": "swo-marketplace-client/1.0",
            "Authorization": "Bearer test-token",
        },
        timeout=10.0,
        transport=mocker.ANY,
    )


def test_env_initialization(monkeypatch, mocker):
    monkeypatch.setenv("MPT_TOKEN", API_TOKEN)
    monkeypatch.setenv("MPT_URL", API_URL)
    mock_client = mocker.patch("mpt_api_client.http.client.Client")

    HTTPClient()  # act

    mock_client.assert_called_once_with(
        base_url=API_URL,
        follow_redirects=True,
        headers={
            "User-Agent": "swo-marketplace-client/1.0",
            "Authorization": f"Bearer {API_TOKEN}",
        },
        timeout=10.0,
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

    result = http_client.request("GET", "/")

    assert result.status_code == codes.OK
    assert json.loads(result.content) == {"message": "Hello, World!"}
    assert success_route.called


@respx.mock
def test_http_call_failure(http_client):
    timeout_route = respx.get(f"{API_URL}/timeout").mock(side_effect=ConnectTimeout("Mock Timeout"))

    with pytest.raises(MPTError, match="HTTP Error: Mock Timeout"):
        http_client.request("GET", "/timeout")

    assert timeout_route.called


def test_http_call_with_json_and_files(mocker, http_client, mock_httpx_response):
    files = {"file": ("test.txt", io.StringIO("file content"), "text/plain")}
    parent_request = mocker.patch.object(
        http_client.httpx_client, "request", autospec=True, return_value=mock_httpx_response
    )

    http_client.request("POST", "/upload", files=files, json={"foo": "bar"})  # act

    called_kwargs = parent_request.call_args[1]
    assert called_kwargs["json"] is None
    sent_files = called_kwargs["files"]
    assert "file" in sent_files
    assert "_attachment_data" in sent_files
    payload_tuple = sent_files["_attachment_data"]
    assert payload_tuple[2] == "application/json"
    assert payload_tuple[1].decode() == '{"foo":"bar"}'


def test_http_call_force_multipart(mocker, http_client):
    json_data = {"foo": "bar"}
    parent_request = mocker.patch.object(http_client.httpx_client, "request", autospec=True)

    http_client.request("POST", "/upload", json=json_data, force_multipart=True)  # act

    called_kwargs = parent_request.call_args[1]
    sent_files = called_kwargs["files"]
    assert called_kwargs["json"] is None
    assert "_attachment_data" in sent_files
    payload_tuple = sent_files["_attachment_data"]
    assert payload_tuple[2] == "application/json"
    assert payload_tuple[1].decode() == '{"foo":"bar"}'
