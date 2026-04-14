import json

import httpx
import pytest
import respx

from mpt_api_client.http.query_options import QueryOptions
from mpt_api_client.http.resource_accessor import AsyncResourceAccessor, ResourceAccessor
from tests.unit.conftest import API_URL, DummyModel

RESOURCE_URL = "/api/v1/test/RES-123"
FULL_URL = f"{API_URL}{RESOURCE_URL}"


@pytest.mark.parametrize(
    ("action", "expected_url"),
    [
        (None, FULL_URL),
        ("complete", f"{FULL_URL}/complete"),
    ],
    ids=["without-action", "with-action"],
)
def test_do_request(http_client, action, expected_url):
    response_data = {"id": "RES-123"}
    with respx.mock:
        mock_route = respx.post(expected_url).mock(
            return_value=httpx.Response(httpx.codes.OK, json=response_data)
        )
        accessor = ResourceAccessor(http_client, RESOURCE_URL, DummyModel)

        result = accessor.do_request("POST", action)

    assert result.json() == response_data
    assert mock_route.call_count == 1


def test_do_request_forwards_json(http_client):
    payload = {"name": "Updated"}
    response_data = {"id": "RES-123", "name": "Updated"}
    with respx.mock:
        mock_route = respx.put(FULL_URL).mock(
            return_value=httpx.Response(httpx.codes.OK, json=response_data)
        )
        accessor = ResourceAccessor(http_client, RESOURCE_URL, DummyModel)

        result = accessor.do_request("PUT", json=payload)

    assert result.json() == response_data
    assert json.loads(mock_route.calls[0].request.content.decode()) == payload


def test_do_request_forwards_query_params(http_client):
    response_data = {"id": "RES-123"}
    with respx.mock:
        mock_route = respx.get(FULL_URL, params={"select": "id"}).mock(
            return_value=httpx.Response(httpx.codes.OK, json=response_data)
        )
        accessor = ResourceAccessor(http_client, RESOURCE_URL, DummyModel)

        result = accessor.do_request("GET", query_params={"select": "id"})

    assert result.json() == response_data
    assert mock_route.call_count == 1


def test_do_request_forwards_headers(http_client):
    response_data = {"id": "RES-123"}
    with respx.mock:
        mock_route = respx.get(FULL_URL).mock(
            return_value=httpx.Response(httpx.codes.OK, json=response_data)
        )
        accessor = ResourceAccessor(http_client, RESOURCE_URL, DummyModel)

        result = accessor.do_request("GET", headers={"X-Custom": "value"})

    assert result.json() == response_data
    assert mock_route.calls[0].request.headers["X-Custom"] == "value"


@pytest.mark.parametrize(
    ("action", "expected_url"),
    [
        (None, FULL_URL),
        ("status", f"{FULL_URL}/status"),
    ],
    ids=["without-action", "with-action"],
)
def test_get(http_client, action, expected_url):
    response_data = {"id": "RES-123", "name": "Test Resource"}
    ok_response = httpx.Response(httpx.codes.OK, json=response_data)
    with respx.mock:
        mock_route = respx.get(expected_url).mock(return_value=ok_response)
        accessor = ResourceAccessor(http_client, RESOURCE_URL, DummyModel)

        result = accessor.get(action)

    assert result.to_dict() == response_data
    assert mock_route.calls[0].request.headers["Accept"] == "application/json"


@pytest.mark.parametrize(
    ("action", "expected_url"),
    [
        (None, FULL_URL),
        ("complete", f"{FULL_URL}/complete"),
    ],
    ids=["without-action", "with-action"],
)
def test_post(http_client, action, expected_url):
    payload = {"name": "New"}
    response_data = {"id": "RES-123", "name": "New"}
    with respx.mock:
        mock_route = respx.post(expected_url).mock(
            return_value=httpx.Response(httpx.codes.OK, json=response_data)
        )
        accessor = ResourceAccessor(http_client, RESOURCE_URL, DummyModel)

        result = accessor.post(action, json=payload)

    assert result.to_dict() == response_data
    assert json.loads(mock_route.calls[0].request.content.decode()) == payload


def test_put(http_client):
    payload = {"name": "Updated"}
    response_data = {"id": "RES-123", "name": "Updated"}
    with respx.mock:
        mock_route = respx.put(FULL_URL).mock(
            return_value=httpx.Response(httpx.codes.OK, json=response_data)
        )
        accessor = ResourceAccessor(http_client, RESOURCE_URL, DummyModel)

        result = accessor.put(json=payload)

    assert result.to_dict() == response_data
    assert json.loads(mock_route.calls[0].request.content.decode()) == payload


def test_delete(http_client):  # noqa: AAA01
    with respx.mock:
        mock_route = respx.delete(FULL_URL).mock(
            return_value=httpx.Response(httpx.codes.NO_CONTENT)
        )
        accessor = ResourceAccessor(http_client, RESOURCE_URL, DummyModel)

        accessor.delete()

    assert mock_route.call_count == 1
    assert mock_route.calls[0].request.method == "DELETE"


@pytest.mark.parametrize(
    ("action", "expected_url"),
    [
        (None, FULL_URL),
        ("complete", f"{FULL_URL}/complete"),
    ],
    ids=["without-action", "with-action"],
)
async def test_async_do_request(async_http_client, action, expected_url):
    response_data = {"id": "RES-123"}
    with respx.mock:
        mock_route = respx.post(expected_url).mock(
            return_value=httpx.Response(httpx.codes.OK, json=response_data)
        )
        accessor = AsyncResourceAccessor(async_http_client, RESOURCE_URL, DummyModel)

        result = await accessor.do_request("POST", action)

    assert result.json() == response_data
    assert mock_route.call_count == 1


@pytest.mark.parametrize(
    ("action", "expected_url"),
    [
        (None, FULL_URL),
        ("status", f"{FULL_URL}/status"),
    ],
    ids=["without-action", "with-action"],
)
async def test_async_get(async_http_client, action, expected_url):
    response_data = {"id": "RES-123", "name": "Test Resource"}
    ok_response = httpx.Response(httpx.codes.OK, json=response_data)
    with respx.mock:
        mock_route = respx.get(expected_url).mock(return_value=ok_response)
        accessor = AsyncResourceAccessor(async_http_client, RESOURCE_URL, DummyModel)

        result = await accessor.get(action)

    assert result.to_dict() == response_data
    assert mock_route.calls[0].request.headers["Accept"] == "application/json"


@pytest.mark.parametrize(
    ("action", "expected_url"),
    [
        (None, FULL_URL),
        ("complete", f"{FULL_URL}/complete"),
    ],
    ids=["without-action", "with-action"],
)
async def test_async_post(async_http_client, action, expected_url):
    payload = {"name": "New"}
    response_data = {"id": "RES-123", "name": "New"}
    with respx.mock:
        mock_route = respx.post(expected_url).mock(
            return_value=httpx.Response(httpx.codes.OK, json=response_data)
        )
        accessor = AsyncResourceAccessor(async_http_client, RESOURCE_URL, DummyModel)

        result = await accessor.post(action, json=payload)

    assert result.to_dict() == response_data
    assert json.loads(mock_route.calls[0].request.content.decode()) == payload


async def test_async_put(async_http_client):
    payload = {"name": "Updated"}
    response_data = {"id": "RES-123", "name": "Updated"}
    with respx.mock:
        mock_route = respx.put(FULL_URL).mock(
            return_value=httpx.Response(httpx.codes.OK, json=response_data)
        )
        accessor = AsyncResourceAccessor(async_http_client, RESOURCE_URL, DummyModel)

        result = await accessor.put(json=payload)

    assert result.to_dict() == response_data
    assert json.loads(mock_route.calls[0].request.content.decode()) == payload


async def test_async_delete(async_http_client):  # noqa: AAA01
    with respx.mock:
        mock_route = respx.delete(FULL_URL).mock(
            return_value=httpx.Response(httpx.codes.NO_CONTENT)
        )
        accessor = AsyncResourceAccessor(async_http_client, RESOURCE_URL, DummyModel)

        await accessor.delete()

    assert mock_route.call_count == 1
    assert mock_route.calls[0].request.method == "DELETE"


async def test_async_get_with_render(async_http_client):
    response_data = {"id": "RES-123", "name": "Test Resource"}
    with respx.mock:
        mock_route = respx.get(f"{FULL_URL}?render()").mock(
            return_value=httpx.Response(httpx.codes.OK, json=response_data)
        )
        accessor = AsyncResourceAccessor(async_http_client, RESOURCE_URL, DummyModel)

        result = await accessor.get(options=QueryOptions(render=True))

    assert result.to_dict() == response_data
    assert mock_route.call_count == 1


def test_get_with_render(http_client):
    response_data = {"id": "RES-123", "name": "Test Resource"}
    with respx.mock:
        mock_route = respx.get(f"{FULL_URL}?render()").mock(
            return_value=httpx.Response(httpx.codes.OK, json=response_data)
        )
        accessor = ResourceAccessor(http_client, RESOURCE_URL, DummyModel)

        result = accessor.get(options=QueryOptions(render=True))

    assert result.to_dict() == response_data
    assert mock_route.call_count == 1
