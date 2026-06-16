import io
import json

import pytest
import respx
from httpx import ConnectTimeout, Request, Response, codes

from mpt_api_client.auth import BearerTokenAuthentication
from mpt_api_client.exceptions import MPTAPIError, MPTError, MPTMaxRetryError
from mpt_api_client.http.async_client import AsyncHTTPClient
from mpt_api_client.http.query_options import QueryOptions
from tests.unit.conftest import API_TOKEN, API_URL


@pytest.fixture
def mock_request():
    return Request("GET", url="/")


@pytest.fixture
def mock_response(mock_request):
    return Response(200, json={"message": "Hello, World!"}, request=mock_request)


def test_async_http_initialization(mocker):
    mock_async_client = mocker.patch("mpt_api_client.http.async_client.AsyncClient")
    authentication = BearerTokenAuthentication(API_TOKEN)

    AsyncHTTPClient(base_url=API_URL, authentication=authentication)  # act

    mock_async_client.assert_called_once_with(
        base_url=API_URL,
        follow_redirects=True,
        headers={"User-Agent": "swo-marketplace-client/1.0"},
        auth=authentication,
        timeout=20.0,
        transport=mocker.ANY,
    )


def test_async_env_base_url_initialization(monkeypatch, mocker):
    monkeypatch.setenv("MPT_API_BASE_URL", API_URL)
    mock_async_client = mocker.patch("mpt_api_client.http.async_client.AsyncClient")

    AsyncHTTPClient(authentication=BearerTokenAuthentication(API_TOKEN))  # act

    mock_async_client.assert_called_once_with(
        base_url=API_URL,
        follow_redirects=True,
        headers={"User-Agent": "swo-marketplace-client/1.0"},
        auth=mocker.ANY,
        timeout=20.0,
        transport=mocker.ANY,
    )


@respx.mock
async def test_async_http_call_success(async_http_client, mock_response):
    success_route = respx.get(f"{API_URL}/").mock(return_value=mock_response)

    result = await async_http_client.request("GET", "/")

    assert result.status_code == codes.OK
    assert json.loads(result.content) == {"message": "Hello, World!"}
    assert success_route.called


@respx.mock
async def test_async_http_call_failure(async_http_client):
    timeout_route = respx.get(f"{API_URL}/timeout").mock(side_effect=ConnectTimeout("Mock Timeout"))

    with pytest.raises(MPTError, match=r"Mock Timeout error after 6 retry attempts."):
        await async_http_client.request("GET", "/timeout")

    assert timeout_route.call_count == 6


async def drain_async_stream(stream_cm):
    async with stream_cm as response:
        return [line async for line in response.aiter_lines()]


@respx.mock
async def test_async_stream_yields_lines(async_http_client):
    body = b'{"id": "ID-1"}\n{"id": "ID-2"}\n'
    streamed = Response(200, content=body)
    stream_route = respx.get(f"{API_URL}/charges").mock(return_value=streamed)

    result = await drain_async_stream(
        async_http_client.stream("GET", "/charges", headers={"Accept": "application/jsonl"})
    )

    request = stream_route.calls[0].request
    assert result == ['{"id": "ID-1"}', '{"id": "ID-2"}']
    assert request.headers["Accept"] == "application/jsonl"


@respx.mock
async def test_async_stream_error_status(async_http_client):
    not_found = Response(404, json={"message": "Not Found"})
    respx.get(f"{API_URL}/charges").mock(return_value=not_found)

    with pytest.raises(MPTAPIError, match=r"404"):
        await drain_async_stream(async_http_client.stream("GET", "/charges"))


@respx.mock
async def test_async_stream_conn_error(async_http_client):
    respx.get(f"{API_URL}/charges").mock(side_effect=ConnectTimeout("Mock Timeout"))

    with pytest.raises(MPTMaxRetryError):
        await drain_async_stream(async_http_client.stream("GET", "/charges"))


async def test_http_call_with_json_and_files(mocker, async_http_client, mock_httpx_response):  # noqa: WPS210
    json_data = {"foo": "bar"}
    files = {"file": ("test.txt", io.StringIO("file content"), "text/plain")}
    parent_request = mocker.patch.object(
        async_http_client.httpx_client, "request", autospec=True, return_value=mock_httpx_response
    )

    await async_http_client.request("POST", "/upload", files=files, json=json_data)  # act

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

    await async_http_client.request("POST", "/upload", json=json_data, force_multipart=True)  # act

    called_kwargs = parent_request.call_args[1]
    sent_files = called_kwargs["files"]
    assert called_kwargs["json"] is None
    assert "_attachment_data" in sent_files
    payload_tuple = sent_files["_attachment_data"]
    assert payload_tuple[2] == "application/json"
    assert payload_tuple[1].decode() == '{"foo":"bar"}'


async def test_request_with_render(mocker, async_http_client, mock_httpx_response):
    parent_request = mocker.patch.object(
        async_http_client.httpx_client, "request", autospec=True, return_value=mock_httpx_response
    )

    await async_http_client.request("GET", "/", options=QueryOptions(render=True))

    called_kwargs = parent_request.call_args[1]
    assert called_kwargs["params"] == "render()"


async def test_request_with_render_and_query_params(mocker, async_http_client, mock_httpx_response):
    parent_request = mocker.patch.object(
        async_http_client.httpx_client, "request", autospec=True, return_value=mock_httpx_response
    )

    await async_http_client.request(
        "GET", "/", query_params={"select": "id,name"}, options=QueryOptions(render=True)
    )

    called_kwargs = parent_request.call_args[1]
    assert called_kwargs["params"] == "select=id%2Cname&render()"
