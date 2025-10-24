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
    AsyncNotifications,
    Audit,
    Billing,
    Catalog,
    Commerce,
    Notifications,
)
from tests.unit.conftest import API_TOKEN, API_URL


def get_mpt_client():
    return MPTClient.from_config(base_url=API_URL, api_token=API_TOKEN)


@pytest.mark.parametrize(
    ("resource_name", "expected_type"),
    [
        ("commerce", Commerce),
        ("catalog", Catalog),
        ("audit", Audit),
        ("billing", Billing),
        ("accounts", Accounts),
        ("notifications", Notifications),
    ],
)
def test_mpt_client(resource_name: str, expected_type: type) -> None:
    mpt = MPTClient.from_config(base_url=API_URL, api_token=API_TOKEN)
    resource = getattr(mpt, resource_name)
    assert isinstance(mpt, MPTClient)
    assert isinstance(resource, expected_type)


def test_mpt_client_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MPT_URL", API_URL)
    monkeypatch.setenv("MPT_TOKEN", API_TOKEN)

    mpt = MPTClient()

    assert isinstance(mpt, MPTClient)
    assert isinstance(mpt.http_client, HTTPClient)


@pytest.mark.parametrize(
    ("resource_name", "expected_type"),
    [
        ("commerce", AsyncCommerce),
        ("catalog", AsyncCatalog),
        ("audit", AsyncAudit),
        ("billing", AsyncBilling),
        ("accounts", AsyncAccounts),
        ("notifications", AsyncNotifications),
    ],
)
def test_async_mpt_client(resource_name: str, expected_type: type) -> None:
    mpt = AsyncMPTClient.from_config(base_url=API_URL, api_token=API_TOKEN)
    resource = getattr(mpt, resource_name)

    assert isinstance(mpt, AsyncMPTClient)
    assert isinstance(resource, expected_type)


def test_async_mpt_client_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MPT_URL", API_URL)
    monkeypatch.setenv("MPT_TOKEN", API_TOKEN)

    mpt = AsyncMPTClient()

    assert isinstance(mpt, AsyncMPTClient)
    assert isinstance(mpt.http_client, AsyncHTTPClient)
