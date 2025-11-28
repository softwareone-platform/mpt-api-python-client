import httpx
import pytest
import respx

from mpt_api_client.resources.accounts.account import AccountsService, AsyncAccountsService
from mpt_api_client.resources.accounts.accounts_users import (
    AccountsUsersService,
    AsyncAccountsUsersService,
)


@pytest.fixture
def account_service(http_client):
    return AccountsService(http_client=http_client)


@pytest.fixture
def async_account_service(async_http_client):
    return AsyncAccountsService(http_client=async_http_client)


@pytest.fixture
def accounts_users_service(http_client):
    return AccountsUsersService(
        http_client=http_client, endpoint_params={"account_id": "ACC-0000-0001"}
    )


@pytest.fixture
def async_accounts_users_service(async_http_client):
    return AsyncAccountsUsersService(
        http_client=async_http_client, endpoint_params={"account_id": "ACC-0000-0001"}
    )


@pytest.mark.parametrize(
    "method", ["get", "create", "update", "enable", "disable", "activate", "deactivate", "validate"]
)
def test_mixins_present(account_service, method):
    result = hasattr(account_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method", ["get", "create", "update", "enable", "disable", "activate", "deactivate", "validate"]
)
def test_async_mixins_present(async_account_service, method):
    result = hasattr(async_account_service, method)

    assert result is True


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("users", AccountsUsersService),
    ],
)
def test_property_services(account_service, service_method, expected_service_class):
    result = getattr(account_service, service_method)("ACC-0000-0001")

    assert isinstance(result, expected_service_class)
    assert result.endpoint_params == {"account_id": "ACC-0000-0001"}


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("users", AsyncAccountsUsersService),
    ],
)
def test_async_property_services(async_account_service, service_method, expected_service_class):
    result = getattr(async_account_service, service_method)("ACC-0000-0001")

    assert isinstance(result, expected_service_class)
    assert result.endpoint_params == {"account_id": "ACC-0000-0001"}


def test_account_create(account_service, tmp_path):  # noqa: WPS210
    account_data = {
        "id": "ACC-0000-0001",
        "name": "Test Account",
    }
    logo_path = tmp_path / "logo.png"
    logo_path.write_bytes(b"fake-logo-data")
    with logo_path.open("rb") as logo_file, respx.mock:
        mock_route = respx.post(account_service.path).mock(
            return_value=httpx.Response(httpx.codes.CREATED, json=account_data)
        )

        result = account_service.create(account_data, file=logo_file)

    request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert request.method == "POST"
    assert request.url.path == "/public/v1/accounts/accounts"
    assert result.to_dict() == account_data


def test_account_update(account_service, tmp_path):  # noqa: WPS210
    account_id = "ACC-0000-0001"
    account_data = {
        "name": "Updated Test Account",
    }
    logo_path = tmp_path / "logo.png"
    logo_path.write_bytes(b"fake-logo-data")
    with logo_path.open("rb") as logo_file, respx.mock:
        mock_route = respx.put(f"{account_service.path}/{account_id}").mock(
            return_value=httpx.Response(httpx.codes.OK, json={"id": account_id, **account_data})
        )

        result = account_service.update(account_id, account_data, file=logo_file)

    request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert request.method == "PUT"
    assert request.url.path == f"/public/v1/accounts/accounts/{account_id}"
    assert result.to_dict() == {"id": account_id, **account_data}


async def test_async_account_create(async_account_service, tmp_path):  # noqa: WPS210
    account_data = {
        "id": "ACC-0000-0001",
        "name": "Test Account",
    }
    logo_path = tmp_path / "logo.png"
    logo_path.write_bytes(b"fake-logo-data")
    with logo_path.open("rb") as logo_file, respx.mock:
        mock_route = respx.post(async_account_service.path).mock(
            return_value=httpx.Response(httpx.codes.CREATED, json=account_data)
        )

        result = await async_account_service.create(account_data, file=logo_file)

    request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert request.method == "POST"
    assert request.url.path == "/public/v1/accounts/accounts"
    assert result.to_dict() == account_data


async def test_async_account_update(async_account_service, tmp_path):  # noqa: WPS210
    account_id = "ACC-0000-0001"
    account_data = {
        "name": "Updated Test Account",
    }
    logo_path = tmp_path / "logo.png"
    logo_path.write_bytes(b"fake-logo-data")
    with logo_path.open("rb") as logo_file, respx.mock:
        mock_route = respx.put(f"{async_account_service.path}/{account_id}").mock(
            return_value=httpx.Response(httpx.codes.OK, json={"id": account_id, **account_data})
        )

        result = await async_account_service.update(account_id, account_data, file=logo_file)

    request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert request.method == "PUT"
    assert request.url.path == f"/public/v1/accounts/accounts/{account_id}"
    assert result.to_dict() == {"id": account_id, **account_data}
