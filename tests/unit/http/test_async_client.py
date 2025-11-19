import io
import json

import pytest
import respx
from httpx import ConnectTimeout, Request, Response, codes

from mpt_api_client.exceptions import MPTError
from mpt_api_client.http.async_client import AsyncHTTPClient
from tests.unit.conftest import API_TOKEN, API_URL


@pytest.fixture
def mock_request():
    return Request("GET", url="/")


@pytest.fixture
def mock_response(mock_request):
    return Response(200, json={"message": "Hello, World!"}, request=mock_request)


def test_async_http_initialization(mocker):
    mock_async_client = mocker.patch("mpt_api_client.http.async_client.AsyncClient")

    AsyncHTTPClient(base_url=API_URL, api_token=API_TOKEN)

    mock_async_client.assert_called_once_with(
        base_url=API_URL,
        follow_redirects=True,
        headers={
            "User-Agent": "swo-marketplace-client/1.0",
            "Authorization": "Bearer test-token",
            "Accept": "application/json",
        },
        timeout=5.0,
        transport=mocker.ANY,
    )


def test_async_env_initialization(monkeypatch, mocker):
    monkeypatch.setenv("MPT_TOKEN", API_TOKEN)
    monkeypatch.setenv("MPT_URL", API_URL)
    mock_async_client = mocker.patch("mpt_api_client.http.async_client.AsyncClient")

    AsyncHTTPClient()

    mock_async_client.assert_called_once_with(
        base_url=API_URL,
        follow_redirects=True,
        headers={
            "User-Agent": "swo-marketplace-client/1.0",
            "Authorization": f"Bearer {API_TOKEN}",
            "Accept": "application/json",
        },
        timeout=5.0,
        transport=mocker.ANY,
    )


def test_async_http_without_token():
    with pytest.raises(ValueError):
        AsyncHTTPClient(base_url=API_URL)


def test_async_http_without_url():
    with pytest.raises(ValueError):
        AsyncHTTPClient(api_token=API_TOKEN)


@respx.mock
async def test_async_http_call_success(async_http_client, mock_response):
    success_route = respx.get(f"{API_URL}/").mock(return_value=mock_response)

    success_response = await async_http_client.request("GET", "/")

    assert success_response.status_code == codes.OK
    assert json.loads(success_response.content) == {"message": "Hello, World!"}
    assert success_route.called


@respx.mock
async def test_async_http_call_failure(async_http_client):
    timeout_route = respx.get(f"{API_URL}/timeout").mock(side_effect=ConnectTimeout("Mock Timeout"))

    with pytest.raises(MPTError, match="HTTP Error: Mock Timeout"):
        await async_http_client.request("GET", "/timeout")

    assert timeout_route.called


async def test_http_call_with_json_and_files(mocker, async_http_client, mock_httpx_response):  # noqa: WPS210
    json_data = {"foo": "bar"}
    files = {"file": ("test.txt", io.StringIO("file content"), "text/plain")}

    parent_request = mocker.patch.object(
        async_http_client.httpx_client, "request", autospec=True, return_value=mock_httpx_response
    )
    await async_http_client.request("POST", "/upload", files=files, json=json_data)

    called_kwargs = parent_request.call_args[1]
    assert called_kwargs["json"] is None
    sent_files = called_kwargs["files"]
    assert "file" in sent_files
    assert "_attachment_data" in sent_files

    payload_tuple = sent_files["_attachment_data"]
    assert payload_tuple[2] == "application/json"
    assert payload_tuple[1].decode() == '{"foo":"bar"}'


async def test_http_call_force_multipart(mocker, async_http_client, mock_httpx_response):  # noqa: WPS210
    json_data = {"foo": "bar"}

    parent_request = mocker.patch.object(
        async_http_client.httpx_client, "request", autospec=True, return_value=mock_httpx_response
    )

    await async_http_client.request("POST", "/upload", json=json_data, force_multipart=True)

    called_kwargs = parent_request.call_args[1]
    sent_files = called_kwargs["files"]

    assert called_kwargs["json"] is None
    assert "_attachment_data" in sent_files

    payload_tuple = sent_files["_attachment_data"]
    assert payload_tuple[2] == "application/json"
    assert payload_tuple[1].decode() == '{"foo":"bar"}'
