import base64
import datetime as dt
import json
from collections.abc import AsyncGenerator

import httpx
import pytest
import respx

from mpt_api_client.auth import ExtensionFrameworkAuthentication
from mpt_api_client.exceptions import MPTAPIError, MPTError
from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from tests.unit.conftest import API_URL

SECRET = "extension-secret"
TOKEN_URL = f"{API_URL}/public/v1/integration/installations/-/token"
ORDERS_URL = f"{API_URL}/orders"


@pytest.fixture
def extension_http_client() -> HTTPClient:
    return HTTPClient(base_url=API_URL, authentication=ExtensionFrameworkAuthentication(SECRET))


@pytest.fixture
def async_extension_http_client() -> AsyncHTTPClient:
    return AsyncHTTPClient(
        base_url=API_URL, authentication=ExtensionFrameworkAuthentication(SECRET)
    )


def _jwt_with_exp(expires_at: dt.datetime, subject: str = "token") -> str:
    def encode(payload: object) -> str:
        raw = json.dumps(payload).encode("utf-8")
        return base64.urlsafe_b64encode(raw).decode("utf-8").rstrip("=")

    claims = {"exp": int(expires_at.timestamp()), "sub": subject}
    return f"{encode({'alg': 'none'})}.{encode(claims)}.signature"


@respx.mock
def test_extension_framework_fetches_and_applies_token(extension_http_client):
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"token": "installation-token"})
    )
    target_route = respx.get(ORDERS_URL).mock(return_value=httpx.Response(200, json={"data": []}))

    extension_http_client.request("GET", "/orders")  # act

    token_request = token_route.calls.last.request
    target_request = target_route.calls.last.request
    assert token_request.headers["Authorization"] == f"Bearer {SECRET}"
    assert target_request.headers["Authorization"] == "Bearer installation-token"


@respx.mock
def test_extension_framework_caches_token_across_requests(extension_http_client):
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"token": "installation-token"})
    )
    respx.get(ORDERS_URL).mock(return_value=httpx.Response(200, json={"data": []}))

    extension_http_client.request("GET", "/orders")  # first call populates the cache

    extension_http_client.request("GET", "/orders")  # act

    assert token_route.call_count == 1


@respx.mock
def test_extension_framework_refreshes_expired_token(extension_http_client):
    token_route = respx.post(TOKEN_URL).mock(
        side_effect=[
            httpx.Response(200, json={"token": "stale-token"}),
            httpx.Response(200, json={"token": "fresh-token"}),
        ]
    )
    target_route = respx.get(ORDERS_URL).mock(
        side_effect=[
            httpx.Response(401, json={"error": "expired"}),
            httpx.Response(200, json={"data": []}),
        ]
    )

    response = extension_http_client.request("GET", "/orders")  # act

    target_request = target_route.calls.last.request
    assert response.status_code == httpx.codes.OK
    assert token_route.call_count == 2
    assert target_request.headers["Authorization"] == "Bearer fresh-token"


@respx.mock
def test_extension_framework_retries_non_idempotent_request_on_unauthorized(
    extension_http_client,
):
    token_route = respx.post(TOKEN_URL).mock(
        side_effect=[
            httpx.Response(200, json={"token": "stale-token"}),
            httpx.Response(200, json={"token": "fresh-token"}),
        ]
    )
    target_route = respx.post(ORDERS_URL).mock(
        side_effect=[
            httpx.Response(401, json={"error": "expired"}),
            httpx.Response(201, json={"id": "ORD-1"}),
        ]
    )

    response = extension_http_client.request("POST", "/orders", json={"x": 1})  # act

    target_request = target_route.calls.last.request
    assert response.status_code == httpx.codes.CREATED
    assert token_route.call_count == 2
    assert target_route.call_count == 2
    assert target_request.headers["Authorization"] == "Bearer fresh-token"


@respx.mock
def test_extension_framework_retry_resends_streamed_body(extension_http_client):
    token_route = respx.post(TOKEN_URL).mock(
        side_effect=[
            httpx.Response(200, json={"token": "stale-token"}),
            httpx.Response(200, json={"token": "fresh-token"}),
        ]
    )
    target_route = respx.post(ORDERS_URL).mock(
        side_effect=[
            httpx.Response(401, json={"error": "expired"}),
            httpx.Response(201, json={"id": "ORD-1"}),
        ]
    )

    result = extension_http_client.httpx_client.request(
        "POST", "/orders", content=iter([b"chunk-1", b"chunk-2"])
    )

    target_request = target_route.calls.last.request
    assert result.status_code == httpx.codes.CREATED
    assert token_route.call_count == 2
    assert target_route.call_count == 2
    assert target_request.headers["Authorization"] == "Bearer fresh-token"
    assert target_request.content == b"chunk-1chunk-2"


@respx.mock
def test_extension_framework_surfaces_repeated_unauthorized(extension_http_client):
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={"token": "any-token"}))
    target_route = respx.get(ORDERS_URL).mock(
        return_value=httpx.Response(401, json={"error": "nope"})
    )

    with pytest.raises(MPTAPIError) as exc_info:  # act
        extension_http_client.request("GET", "/orders")

    assert exc_info.value.status_code == httpx.codes.UNAUTHORIZED
    assert target_route.call_count == 2  # original + exactly one retry, then surfaced


@respx.mock
async def test_extension_framework_works_with_async_client(async_extension_http_client):
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"token": "installation-token"})
    )
    target_route = respx.get(ORDERS_URL).mock(return_value=httpx.Response(200, json={"data": []}))

    await async_extension_http_client.request("GET", "/orders")  # act

    target_request = target_route.calls.last.request
    assert token_route.called
    assert target_request.headers["Authorization"] == "Bearer installation-token"


@respx.mock
async def test_extension_framework_caches_token_across_requests_async(
    async_extension_http_client,
):
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"token": "installation-token"})
    )
    respx.get(ORDERS_URL).mock(return_value=httpx.Response(200, json={"data": []}))

    await async_extension_http_client.request("GET", "/orders")  # first call populates the cache

    await async_extension_http_client.request("GET", "/orders")  # act

    assert token_route.call_count == 1


@respx.mock
async def test_extension_framework_refreshes_expired_token_async(async_extension_http_client):
    token_route = respx.post(TOKEN_URL).mock(
        side_effect=[
            httpx.Response(200, json={"token": "stale-token"}),
            httpx.Response(200, json={"token": "fresh-token"}),
        ]
    )
    target_route = respx.get(ORDERS_URL).mock(
        side_effect=[
            httpx.Response(401, json={"error": "expired"}),
            httpx.Response(200, json={"data": []}),
        ]
    )

    response = await async_extension_http_client.request("GET", "/orders")  # act

    target_request = target_route.calls.last.request
    assert response.status_code == httpx.codes.OK
    assert token_route.call_count == 2
    assert target_request.headers["Authorization"] == "Bearer fresh-token"


@respx.mock
async def test_extension_framework_retries_non_idempotent_request_on_unauthorized_async(
    async_extension_http_client,
):
    token_route = respx.post(TOKEN_URL).mock(
        side_effect=[
            httpx.Response(200, json={"token": "stale-token"}),
            httpx.Response(200, json={"token": "fresh-token"}),
        ]
    )
    target_route = respx.post(ORDERS_URL).mock(
        side_effect=[
            httpx.Response(401, json={"error": "expired"}),
            httpx.Response(201, json={"id": "ORD-1"}),
        ]
    )

    response = await async_extension_http_client.request("POST", "/orders", json={"x": 1})  # act

    target_request = target_route.calls.last.request
    assert response.status_code == httpx.codes.CREATED
    assert token_route.call_count == 2
    assert target_route.call_count == 2
    assert target_request.headers["Authorization"] == "Bearer fresh-token"


@respx.mock
async def test_extension_framework_retry_resends_streamed_body_async(async_extension_http_client):
    token_route = respx.post(TOKEN_URL).mock(
        side_effect=[
            httpx.Response(200, json={"token": "stale-token"}),
            httpx.Response(200, json={"token": "fresh-token"}),
        ]
    )
    target_route = respx.post(ORDERS_URL).mock(
        side_effect=[
            httpx.Response(401, json={"error": "expired"}),
            httpx.Response(201, json={"id": "ORD-1"}),
        ]
    )

    # httpx AsyncClient requires an async iterable for streamed content
    async def stream_body() -> AsyncGenerator[bytes]:  # noqa: RUF029
        yield b"chunk-1"
        yield b"chunk-2"

    result = await async_extension_http_client.httpx_client.request(
        "POST", "/orders", content=stream_body()
    )

    target_request = target_route.calls.last.request
    assert result.status_code == httpx.codes.CREATED
    assert token_route.call_count == 2
    assert target_route.call_count == 2
    assert target_request.headers["Authorization"] == "Bearer fresh-token"
    assert target_request.content == b"chunk-1chunk-2"


@respx.mock
async def test_extension_framework_surfaces_repeated_unauthorized_async(
    async_extension_http_client,
):
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={"token": "any-token"}))
    target_route = respx.get(ORDERS_URL).mock(
        return_value=httpx.Response(401, json={"error": "nope"})
    )

    with pytest.raises(MPTAPIError) as exc_info:  # act
        await async_extension_http_client.request("GET", "/orders")

    assert exc_info.value.status_code == httpx.codes.UNAUTHORIZED
    assert target_route.call_count == 2  # original + exactly one retry, then surfaced


@respx.mock
def test_extension_framework_token_error(extension_http_client):
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(403, json={"error": "forbidden"}))

    with pytest.raises(MPTError):  # act
        extension_http_client.request("GET", "/orders")


def test_extension_framework_requires_configuration():
    provider = ExtensionFrameworkAuthentication(SECRET)
    auth_flow = provider.sync_auth_flow(httpx.Request("GET", ORDERS_URL))

    with pytest.raises(MPTError):  # act
        next(auth_flow)


@respx.mock
def test_extension_framework_rejects_empty_token(extension_http_client):
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={"token": None}))

    with pytest.raises(MPTError):  # act
        extension_http_client.request("GET", "/orders")


@respx.mock
def test_extension_framework_account_scoped_token_request():
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"token": "account-token"})
    )
    respx.get(ORDERS_URL).mock(return_value=httpx.Response(200, json={"data": []}))
    client = HTTPClient(
        base_url=API_URL,
        authentication=ExtensionFrameworkAuthentication(SECRET, account_id="ACC-123"),
    )

    client.request("GET", "/orders")  # act

    token_request = token_route.calls.last.request
    assert token_request.url.params["account.id"] == "ACC-123"


@respx.mock
def test_extension_framework_refreshes_proactively_before_expiry(extension_http_client):
    near_expiry = dt.datetime.now(dt.UTC) + dt.timedelta(seconds=10)
    far_expiry = dt.datetime.now(dt.UTC) + dt.timedelta(hours=1)
    token_route = respx.post(TOKEN_URL).mock(
        side_effect=[
            httpx.Response(200, json={"token": _jwt_with_exp(near_expiry, "stale")}),
            httpx.Response(200, json={"token": _jwt_with_exp(far_expiry, "fresh")}),
        ]
    )
    respx.get(ORDERS_URL).mock(return_value=httpx.Response(200, json={"data": []}))

    extension_http_client.request("GET", "/orders")  # first call caches a near-expiry token

    extension_http_client.request("GET", "/orders")  # act: token within leeway -> refresh

    assert token_route.call_count == 2


@respx.mock
def test_extension_framework_reuses_unexpired_token(extension_http_client):
    far_expiry = dt.datetime.now(dt.UTC) + dt.timedelta(hours=1)
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"token": _jwt_with_exp(far_expiry)})
    )
    respx.get(ORDERS_URL).mock(return_value=httpx.Response(200, json={"data": []}))

    extension_http_client.request("GET", "/orders")  # caches a long-lived token

    extension_http_client.request("GET", "/orders")  # act

    assert token_route.call_count == 1
