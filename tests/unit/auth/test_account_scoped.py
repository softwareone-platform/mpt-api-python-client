import asyncio
import base64
import datetime as dt
import json

import httpx
import pytest
import respx

from mpt_api_client.auth import AccountScopedAuthentication
from mpt_api_client.exceptions import MPTAPIError, MPTError
from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from tests.unit.conftest import API_URL

SECRET = "extension-secret"
ACCOUNT_ID = "ACC-1"
TOKEN_URL = f"{API_URL}/public/v1/integration/installations/-/token"
ORDERS_URL = f"{API_URL}/orders"


def _jwt_with_exp(expires_at: dt.datetime, subject: str = "token") -> str:
    def encode(payload: object) -> str:
        raw = json.dumps(payload).encode("utf-8")
        return base64.urlsafe_b64encode(raw).decode("utf-8").rstrip("=")

    claims = {"exp": int(expires_at.timestamp()), "sub": subject}
    return f"{encode({'alg': 'none'})}.{encode(claims)}.signature"


pytestmark = pytest.mark.usefixtures("_clear_account_cache")


@pytest.fixture
def _clear_account_cache():
    AccountScopedAuthentication.clear_cache()
    yield
    AccountScopedAuthentication.clear_cache()


@respx.mock
def test_account_scoped_applies_token_and_sends_account_id():
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"token": "account-token"})
    )
    target_route = respx.get(ORDERS_URL).mock(return_value=httpx.Response(200, json={"data": []}))
    client = HTTPClient(
        base_url=API_URL,
        authentication=AccountScopedAuthentication(SECRET, account_id=ACCOUNT_ID),
    )

    client.request("GET", "/orders")  # act

    token_request = token_route.calls.last.request
    target_request = target_route.calls.last.request
    assert token_request.headers["Authorization"] == f"Bearer {SECRET}"
    assert token_request.url.params["account.id"] == ACCOUNT_ID
    assert target_request.headers["Authorization"] == "Bearer account-token"


@respx.mock
def test_shared_cache_across_clients_fetches_token_once():
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"token": "account-token"})
    )
    respx.get(ORDERS_URL).mock(return_value=httpx.Response(200, json={"data": []}))
    first_client = HTTPClient(
        base_url=API_URL,
        authentication=AccountScopedAuthentication(SECRET, account_id=ACCOUNT_ID),
    )
    second_client = HTTPClient(
        base_url=API_URL,
        authentication=AccountScopedAuthentication(SECRET, account_id=ACCOUNT_ID),
    )

    first_client.request("GET", "/orders")  # populates the shared cache

    second_client.request("GET", "/orders")  # act: reuses the cached token

    assert token_route.call_count == 1


@respx.mock
def test_different_accounts_fetch_separate_tokens():
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"token": "account-token"})
    )
    respx.get(ORDERS_URL).mock(return_value=httpx.Response(200, json={"data": []}))
    first_client = HTTPClient(
        base_url=API_URL,
        authentication=AccountScopedAuthentication(SECRET, account_id="ACC-1"),
    )
    second_client = HTTPClient(
        base_url=API_URL,
        authentication=AccountScopedAuthentication(SECRET, account_id="ACC-2"),
    )

    first_client.request("GET", "/orders")

    second_client.request("GET", "/orders")  # act: different scope, separate token

    assert token_route.call_count == 2
    fetched_accounts = {call.request.url.params["account.id"] for call in token_route.calls}
    assert fetched_accounts == {"ACC-1", "ACC-2"}


@respx.mock
async def test_serialized_refresh_fetches_token_once_under_concurrency():
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"token": "account-token"})
    )
    respx.get(ORDERS_URL).mock(return_value=httpx.Response(200, json={"data": []}))
    client = AsyncHTTPClient(
        base_url=API_URL,
        authentication=AccountScopedAuthentication(SECRET, account_id=ACCOUNT_ID),
    )

    await asyncio.gather(*(client.request("GET", "/orders") for _ in range(10)))  # act

    assert token_route.call_count == 1


@respx.mock
def test_refreshes_proactively_before_expiry():
    near_expiry = dt.datetime.now(dt.UTC) + dt.timedelta(seconds=10)
    far_expiry = dt.datetime.now(dt.UTC) + dt.timedelta(hours=1)
    token_route = respx.post(TOKEN_URL).mock(
        side_effect=[
            httpx.Response(200, json={"token": _jwt_with_exp(near_expiry, "stale")}),
            httpx.Response(200, json={"token": _jwt_with_exp(far_expiry, "fresh")}),
        ]
    )
    respx.get(ORDERS_URL).mock(return_value=httpx.Response(200, json={"data": []}))
    client = HTTPClient(
        base_url=API_URL,
        authentication=AccountScopedAuthentication(SECRET, account_id=ACCOUNT_ID),
    )

    client.request("GET", "/orders")  # caches a near-expiry token

    client.request("GET", "/orders")  # act: token within leeway -> proactive refresh

    assert token_route.call_count == 2


@respx.mock
def test_reuses_unexpired_token():
    far_expiry = dt.datetime.now(dt.UTC) + dt.timedelta(hours=1)
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"token": _jwt_with_exp(far_expiry)})
    )
    respx.get(ORDERS_URL).mock(return_value=httpx.Response(200, json={"data": []}))
    client = HTTPClient(
        base_url=API_URL,
        authentication=AccountScopedAuthentication(SECRET, account_id=ACCOUNT_ID),
    )

    client.request("GET", "/orders")  # caches a long-lived token

    client.request("GET", "/orders")  # act

    assert token_route.call_count == 1


@respx.mock
def test_reactive_refresh_on_unauthorized():
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
    client = HTTPClient(
        base_url=API_URL,
        authentication=AccountScopedAuthentication(SECRET, account_id=ACCOUNT_ID),
    )

    response = client.request("GET", "/orders")  # act

    target_request = target_route.calls.last.request
    assert response.status_code == httpx.codes.OK
    assert token_route.call_count == 2
    assert target_request.headers["Authorization"] == "Bearer fresh-token"


@respx.mock
def test_surfaces_repeated_unauthorized():
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={"token": "any-token"}))
    target_route = respx.get(ORDERS_URL).mock(
        return_value=httpx.Response(401, json={"error": "nope"})
    )
    client = HTTPClient(
        base_url=API_URL,
        authentication=AccountScopedAuthentication(SECRET, account_id=ACCOUNT_ID),
    )

    with pytest.raises(MPTAPIError) as exc_info:  # act
        client.request("GET", "/orders")

    assert exc_info.value.status_code == httpx.codes.UNAUTHORIZED
    assert target_route.call_count == 2  # original + exactly one retry, then surfaced


@respx.mock
async def test_reactive_refresh_on_unauthorized_async():
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
    client = AsyncHTTPClient(
        base_url=API_URL,
        authentication=AccountScopedAuthentication(SECRET, account_id=ACCOUNT_ID),
    )

    response = await client.request("GET", "/orders")  # act

    target_request = target_route.calls.last.request
    assert response.status_code == httpx.codes.OK
    assert token_route.call_count == 2
    assert target_request.headers["Authorization"] == "Bearer fresh-token"


@respx.mock
def test_rejects_empty_token():
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={"token": None}))
    client = HTTPClient(
        base_url=API_URL,
        authentication=AccountScopedAuthentication(SECRET, account_id=ACCOUNT_ID),
    )

    with pytest.raises(MPTError):  # act
        client.request("GET", "/orders")


def test_requires_configuration():
    provider = AccountScopedAuthentication(SECRET, account_id=ACCOUNT_ID)
    auth_flow = provider.sync_auth_flow(httpx.Request("GET", ORDERS_URL))

    with pytest.raises(MPTError):  # act
        next(auth_flow)


def test_store_evicts_expired_entries():
    past = dt.datetime.now(dt.UTC) - dt.timedelta(hours=1)
    future = dt.datetime.now(dt.UTC) + dt.timedelta(hours=1)
    stale_provider = AccountScopedAuthentication(SECRET, account_id="ACC-OLD")
    fresh_provider = AccountScopedAuthentication(SECRET, account_id="ACC-NEW")

    stale_provider._store(_jwt_with_exp(past))  # noqa: SLF001
    fresh_provider._store(_jwt_with_exp(future))  # noqa: SLF001 ; act: triggers eviction

    cache = AccountScopedAuthentication._token_cache  # noqa: SLF001
    assert (SECRET, "ACC-OLD") not in cache
    assert (SECRET, "ACC-NEW") in cache
