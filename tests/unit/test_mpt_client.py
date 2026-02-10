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

    result = getattr(mpt, resource_name)

    assert isinstance(mpt, MPTClient)
    assert isinstance(result, expected_type)


def test_mpt_client_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MPT_API_BASE_URL", API_URL)
    monkeypatch.setenv("MPT_API_TOKEN", API_TOKEN)

    result = MPTClient()

    assert isinstance(result, MPTClient)
    assert isinstance(result.http_client, HTTPClient)


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

    result = getattr(mpt, resource_name)

    assert isinstance(mpt, AsyncMPTClient)
    assert isinstance(result, expected_type)


def test_async_mpt_client_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MPT_API_BASE_URL", API_URL)
    monkeypatch.setenv("MPT_API_TOKEN", API_TOKEN)

    result = AsyncMPTClient()

    assert isinstance(result, AsyncMPTClient)
    assert isinstance(result.http_client, AsyncHTTPClient)
