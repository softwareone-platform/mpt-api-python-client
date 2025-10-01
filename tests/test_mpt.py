import pytest

from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.mpt_client import AsyncMPTClient, MPTClient
from mpt_api_client.resources import (
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


def test_mpt_client() -> None:
    mpt = MPTClient.from_config(base_url=API_URL, api_token=API_TOKEN)
    commerce = mpt.commerce
    catalog = mpt.catalog
    audit = mpt.audit
    billing = mpt.billing

    assert isinstance(mpt, MPTClient)
    assert isinstance(commerce, Commerce)
    assert isinstance(catalog, Catalog)
    assert isinstance(audit, Audit)
    assert isinstance(billing, Billing)


def test_mpt_client_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MPT_URL", API_URL)
    monkeypatch.setenv("MPT_TOKEN", API_TOKEN)

    mpt = MPTClient()

    assert isinstance(mpt, MPTClient)
    assert isinstance(mpt.http_client, HTTPClient)


def test_async_mpt_client() -> None:
    mpt = AsyncMPTClient.from_config(base_url=API_URL, api_token=API_TOKEN)
    commerce = mpt.commerce
    catalog = mpt.catalog
    audit = mpt.audit
    billing = mpt.billing

    assert isinstance(mpt, AsyncMPTClient)
    assert isinstance(commerce, AsyncCommerce)
    assert isinstance(catalog, AsyncCatalog)
    assert isinstance(audit, AsyncAudit)
    assert isinstance(billing, AsyncBilling)


def test_async_mpt_client_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MPT_URL", API_URL)
    monkeypatch.setenv("MPT_TOKEN", API_TOKEN)

    mpt = AsyncMPTClient()

    assert isinstance(mpt, AsyncMPTClient)
    assert isinstance(mpt.http_client, AsyncHTTPClient)
