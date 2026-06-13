import httpx
import pytest
import respx

from mpt_api_client.exceptions import MPTError
from mpt_api_client.http import (
    AsyncHTTPClient,
    BearerTokenAuthentication,
    ExtensionFrameworkAuthentication,
    HTTPClient,
)
from tests.unit.conftest import API_URL

SECRET = "extension-secret"
TOKEN_URL = f"{API_URL}/public/v1/integration/installations/-/token"
ORDERS_URL = f"{API_URL}/orders"


def test_bearer_token_sets_authorization_header():
    authentication = BearerTokenAuthentication("my-token")
    request = httpx.Request("GET", f"{API_URL}/")

    sent = next(authentication.auth_flow(request))  # act

    assert sent.headers["Authorization"] == "Bearer my-token"


@respx.mock
def test_extension_framework_fetches_and_applies_token():
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"token": "installation-token"})
    )
    target_route = respx.get(ORDERS_URL).mock(return_value=httpx.Response(200, json={"data": []}))
    client = HTTPClient(base_url=API_URL, authentication=ExtensionFrameworkAuthentication(SECRET))

    client.request("GET", "/orders")  # act

    token_request = token_route.calls.last.request
    target_request = target_route.calls.last.request
    assert token_request.headers["Authorization"] == f"Bearer {SECRET}"
    assert target_request.headers["Authorization"] == "Bearer installation-token"


@respx.mock
def test_extension_framework_caches_token_across_requests():
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"token": "installation-token"})
    )
    respx.get(ORDERS_URL).mock(return_value=httpx.Response(200, json={"data": []}))
    client = HTTPClient(base_url=API_URL, authentication=ExtensionFrameworkAuthentication(SECRET))

    client.request("GET", "/orders")  # first call populates the cache

    client.request("GET", "/orders")  # act

    assert token_route.call_count == 1


@respx.mock
def test_extension_framework_refreshes_expired_token():
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
    client = HTTPClient(base_url=API_URL, authentication=ExtensionFrameworkAuthentication(SECRET))

    response = client.request("GET", "/orders")  # act

    target_request = target_route.calls.last.request
    assert response.status_code == httpx.codes.OK
    assert token_route.call_count == 2
    assert target_request.headers["Authorization"] == "Bearer fresh-token"


@respx.mock
async def test_extension_framework_works_with_async_client():
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"token": "installation-token"})
    )
    target_route = respx.get(ORDERS_URL).mock(return_value=httpx.Response(200, json={"data": []}))
    client = AsyncHTTPClient(
        base_url=API_URL, authentication=ExtensionFrameworkAuthentication(SECRET)
    )

    await client.request("GET", "/orders")  # act

    target_request = target_route.calls.last.request
    assert token_route.called
    assert target_request.headers["Authorization"] == "Bearer installation-token"


@respx.mock
def test_extension_framework_token_error():
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(403, json={"error": "forbidden"}))
    client = HTTPClient(base_url=API_URL, authentication=ExtensionFrameworkAuthentication(SECRET))

    with pytest.raises(MPTError):  # act
        client.request("GET", "/orders")
