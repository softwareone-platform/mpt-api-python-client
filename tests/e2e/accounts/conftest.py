import datetime as dt

import pytest


@pytest.fixture(scope="session")
def timestamp():
    return int(dt.datetime.now(tz=dt.UTC).strftime("%Y%m%d%H%M%S"))


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
