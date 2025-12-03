import datetime as dt

import pytest

from mpt_api_client.exceptions import MPTAPIError


@pytest.fixture(scope="session")
def timestamp():
    return int(dt.datetime.now(tz=dt.UTC).strftime("%Y%m%d%H%M%S"))


@pytest.fixture
def invalid_user_id():
    # Used in e2e tests for two resources (users and accounts-users)
    return "USR-0000-0000"


@pytest.fixture
def account_icon(logo_fd):
    return logo_fd


@pytest.fixture
def currencies():
    return ["USD", "EUR"]


@pytest.fixture
def account_id(e2e_config):
    return e2e_config["accounts.account.id"]


@pytest.fixture
def seller_id(e2e_config):
    return e2e_config["accounts.seller.id"]


@pytest.fixture
def buyer_id(e2e_config):
    return e2e_config["accounts.buyer.id"]


@pytest.fixture
def user_group_id(e2e_config):
    return e2e_config["accounts.user_group.id"]


@pytest.fixture
def module_id(e2e_config):
    return e2e_config["accounts.module.id"]


@pytest.fixture
def user_id(e2e_config):
    return e2e_config["accounts.user.id"]


@pytest.fixture
def user_group_factory(account_id, module_id):
    # Used in user group and licensee fixtures
    def _user_group(
        name: str = "E2E Test Api Client User Group",
        user_group_account_id: str = account_id,
    ):
        return {
            "name": name,
            "account": {"id": user_group_account_id},
            "buyers": None,
            "logo": "",
            "description": "User group for E2E tests",
            "modules": [{"id": module_id}],
        }

    return _user_group


@pytest.fixture
def account_user_factory(account_id, user_group_id, uuid_str):
    def _account_user(  # noqa: WPS430
        email: str | None = None,  # Must be unique in Marketplace
        first_name: str = "E2E Created",
        last_name: str = "Account User",
    ):
        if not email:
            email = f"e2e_{uuid_str}@dummy.com"

        return {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
            },
            "account": {
                "id": account_id,
            },
            "groups": [
                {"id": user_group_id},
            ],
            "invitation": {
                "status": "Invited",
            },
        }

    return _account_user


@pytest.fixture
def created_account_user(mpt_vendor, account_user_factory, account_id):
    """Fixture to create and teardown an account user used in two resources."""
    ret_account_user = None

    def _created_account_user(
        first_name: str = "E2E Created",
        last_name: str = "Account User",
    ):
        """Create an account user with the given first and last name."""
        nonlocal ret_account_user  # noqa: WPS420
        account_user_data = account_user_factory(
            first_name=first_name,
            last_name=last_name,
        )
        users_obj = mpt_vendor.accounts.accounts.users(account_id=account_id)
        ret_account_user = users_obj.create(account_user_data)
        return ret_account_user

    yield _created_account_user

    if ret_account_user:
        users_obj = mpt_vendor.accounts.accounts.users(account_id=account_id)
        try:
            users_obj.delete(ret_account_user.id)
        except MPTAPIError:
            print(  # noqa: WPS421
                f"TEARDOWN - Unable to delete account user {ret_account_user.id}",
            )


@pytest.fixture
async def async_created_account_user(async_mpt_vendor, account_user_factory, account_id):
    """Fixture to create and teardown an account user used in two resources."""
    ret_account_user = None

    async def _created_account_user(
        first_name: str = "E2E Created",
        last_name: str = "Account User",
    ):
        """Create an account user with the given first and last name."""
        nonlocal ret_account_user  # noqa: WPS420
        account_user_data = account_user_factory(
            first_name=first_name,
            last_name=last_name,
        )
        users_obj = async_mpt_vendor.accounts.accounts.users(account_id=account_id)
        ret_account_user = await users_obj.create(account_user_data)
        return ret_account_user

    yield _created_account_user

    if ret_account_user:
        users_obj = async_mpt_vendor.accounts.accounts.users(account_id=account_id)
        try:
            await users_obj.delete(ret_account_user.id)
        except MPTAPIError as error:
            print(  # noqa: WPS421
                f"TEARDOWN - Unable to delete account user {ret_account_user.id}: "
                f"{getattr(error, 'title', str(error))}"
            )
