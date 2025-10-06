import pytest

from mpt_api_client.resources.accounts.account import AccountsService, AsyncAccountsService
from mpt_api_client.resources.accounts.accounts import Accounts, AsyncAccounts
from mpt_api_client.resources.accounts.api_tokens import (
    ApiTokensService,
    AsyncApiTokensService,
)
from mpt_api_client.resources.accounts.cloud_tenants import (
    AsyncCloudTenantsService,
    CloudTenantsService,
)
from mpt_api_client.resources.accounts.licensees import AsyncLicenseesService, LicenseesService
from mpt_api_client.resources.accounts.modules import AsyncModulesService, ModulesService
from mpt_api_client.resources.accounts.sellers import AsyncSellersService, SellersService
from mpt_api_client.resources.accounts.user_groups import (
    AsyncUserGroupsService,
    UserGroupsService,
)
from mpt_api_client.resources.accounts.users import AsyncUsersService, UsersService


@pytest.fixture
def accounts(http_client):
    return Accounts(http_client=http_client)


@pytest.fixture
def async_accounts(async_http_client):
    return AsyncAccounts(http_client=async_http_client)


@pytest.mark.parametrize(
    ("property_name", "expected_service_class"),
    [
        ("accounts", AccountsService),
        ("users", UsersService),
        ("sellers", SellersService),
        ("licensees", LicenseesService),
        ("user_groups", UserGroupsService),
        ("api_tokens", ApiTokensService),
        ("modules", ModulesService),
        ("cloud_tenants", CloudTenantsService),
    ],
)
def test_accounts_properties(accounts, property_name, expected_service_class):
    """Test that Accounts properties return correct instances."""
    service = getattr(accounts, property_name)

    assert isinstance(service, expected_service_class)
    assert service.http_client is accounts.http_client


@pytest.mark.parametrize(
    ("property_name", "expected_service_class"),
    [
        ("accounts", AsyncAccountsService),
        ("users", AsyncUsersService),
        ("sellers", AsyncSellersService),
        ("licensees", AsyncLicenseesService),
        ("user_groups", AsyncUserGroupsService),
        ("api_tokens", AsyncApiTokensService),
        ("modules", AsyncModulesService),
        ("cloud_tenants", AsyncCloudTenantsService),
    ],
)
def test_async_accounts_properties(async_accounts, property_name, expected_service_class):
    """Test that AsyncAccounts properties return correct instances."""
    service = getattr(async_accounts, property_name)

    assert isinstance(service, expected_service_class)
    assert service.http_client is async_accounts.http_client


def test_accounts_initialization(http_client):
    accounts = Accounts(http_client=http_client)

    assert accounts.http_client is http_client
    assert isinstance(accounts, Accounts)


def test_async_accounts_initialization(async_http_client):
    accounts = AsyncAccounts(http_client=async_http_client)

    assert accounts.http_client is async_http_client
    assert isinstance(accounts, AsyncAccounts)
