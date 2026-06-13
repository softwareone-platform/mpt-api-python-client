import io
import json

import pytest
import respx
from httpx import ConnectTimeout, Response, codes

from mpt_api_client.exceptions import MPTAPIError, MPTMaxRetryError
from mpt_api_client.http import BearerTokenAuthentication
from mpt_api_client.http.client import HTTPClient
from mpt_api_client.http.query_options import QueryOptions
from tests.unit.conftest import API_TOKEN, API_URL


def test_http_initialization(mocker):
    mock_client = mocker.patch("mpt_api_client.http.client.Client")
    authentication = BearerTokenAuthentication(API_TOKEN)

    HTTPClient(base_url=API_URL, authentication=authentication)  # act

    mock_client.assert_called_once_with(
        base_url=API_URL,
        follow_redirects=True,
        headers={"User-Agent": "swo-marketplace-client/1.0"},
        auth=authentication,
        timeout=20.0,
        transport=mocker.ANY,
    )


def test_env_base_url_initialization(monkeypatch, mocker):
    monkeypatch.setenv("MPT_API_BASE_URL", API_URL)
    mock_client = mocker.patch("mpt_api_client.http.client.Client")

    HTTPClient(authentication=BearerTokenAuthentication(API_TOKEN))  # act

    mock_client.assert_called_once_with(
        base_url=API_URL,
        follow_redirects=True,
        headers={"User-Agent": "swo-marketplace-client/1.0"},
        auth=mocker.ANY,
        timeout=20.0,
        transport=mocker.ANY,
    )


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

    with pytest.raises(MPTMaxRetryError, match=r"Mock Timeout error after 6 retry attempts."):
        http_client.request("GET", "/timeout")

    assert timeout_route.call_count == 6


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


def drain_stream(stream_cm):
    with stream_cm as response:
        return list(response.iter_lines())


@respx.mock
def test_stream_yields_lines(http_client):
    body = b'{"id": "ID-1"}\n{"id": "ID-2"}\n'
    streamed = Response(200, content=body)
    stream_route = respx.get(f"{API_URL}/charges").mock(return_value=streamed)

    result = drain_stream(
        http_client.stream("GET", "/charges", headers={"Accept": "application/jsonl"})
    )

    request = stream_route.calls[0].request
    assert result == ['{"id": "ID-1"}', '{"id": "ID-2"}']
    assert request.headers["Accept"] == "application/jsonl"


@respx.mock
def test_stream_raises_on_error_status(http_client):
    not_found = Response(404, json={"message": "Not Found"})
    respx.get(f"{API_URL}/charges").mock(return_value=not_found)

    with pytest.raises(MPTAPIError, match=r"404"):
        drain_stream(http_client.stream("GET", "/charges"))


@respx.mock
def test_stream_raises_on_connection_error(http_client):
    respx.get(f"{API_URL}/charges").mock(side_effect=ConnectTimeout("Mock Timeout"))

    with pytest.raises(MPTMaxRetryError):
        drain_stream(http_client.stream("GET", "/charges"))


def test_request_with_render(mocker, http_client, mock_httpx_response):
    parent_request = mocker.patch.object(
        http_client.httpx_client, "request", autospec=True, return_value=mock_httpx_response
    )
    http_client.request("GET", "/", options=QueryOptions(render=True))

    result = parent_request.call_args[1]

    assert result["params"] == "render()"


def test_request_with_render_and_query_params(mocker, http_client, mock_httpx_response):
    parent_request = mocker.patch.object(
        http_client.httpx_client, "request", autospec=True, return_value=mock_httpx_response
    )
    http_client.request(
        "GET", "/", query_params={"select": "id,name"}, options=QueryOptions(render=True)
    )

    result = parent_request.call_args[1]

    assert result["params"] == "select=id%2Cname&render()"
