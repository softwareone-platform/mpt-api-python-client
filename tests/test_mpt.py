import pytest

from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.mpt_client import AsyncMPTClient, MPTClient
from mpt_api_client.resources import (
    Accounts,
    AsyncAccounts,
    AsyncAudit,
    AsyncBilling,
    AsyncCatalog,
    AsyncCommerce,
    Audit,
    Billing,
    Catalog,
    Commerce,
)
from tests.conftest import API_TOKEN, API_URL


def get_mpt_client():
    return MPTClient.from_config(base_url=API_URL, api_token=API_TOKEN)


def get_async_mpt_client():
    return AsyncMPTClient.from_config(base_url=API_URL, api_token=API_TOKEN)


@pytest.mark.parametrize(
    ("domain_module", "domain_type"),
    [
        (get_mpt_client(), MPTClient),
        (get_mpt_client().commerce, Commerce),
        (get_mpt_client().catalog, Catalog),
        (get_mpt_client().audit, Audit),
        (get_mpt_client().billing, Billing),
        (get_mpt_client().accounts, Accounts),
    ],
)
def test_mpt_client(domain_module, domain_type) -> None:
    assert isinstance(domain_module, domain_type)


def test_mpt_client_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MPT_URL", API_URL)
    monkeypatch.setenv("MPT_TOKEN", API_TOKEN)

    mpt = MPTClient()

    assert isinstance(mpt, MPTClient)
    assert isinstance(mpt.http_client, HTTPClient)


@pytest.mark.parametrize(
    ("domain_module", "domain_type"),
    [
        (get_async_mpt_client(), AsyncMPTClient),
        (get_async_mpt_client().commerce, AsyncCommerce),
        (get_async_mpt_client().catalog, AsyncCatalog),
        (get_async_mpt_client().audit, AsyncAudit),
        (get_async_mpt_client().billing, AsyncBilling),
        (get_async_mpt_client().accounts, AsyncAccounts),
    ],
)
def test_async_mpt_client(domain_module, domain_type) -> None:
    assert isinstance(domain_module, domain_type)


def test_async_mpt_client_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MPT_URL", API_URL)
    monkeypatch.setenv("MPT_TOKEN", API_TOKEN)

    mpt = AsyncMPTClient()

    assert isinstance(mpt, AsyncMPTClient)
    assert isinstance(mpt.http_client, AsyncHTTPClient)
