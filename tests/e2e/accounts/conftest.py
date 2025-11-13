import datetime as dt
import pathlib

import pytest


@pytest.fixture(scope="session")
def timestamp():
    return int(dt.datetime.now(tz=dt.UTC).strftime("%Y%m%d%H%M%S"))


@pytest.fixture
def account_icon():
    icon_path = pathlib.Path(__file__).parents[1] / "logo.png"
    return pathlib.Path.open(icon_path, "rb")


@pytest.fixture
def currencies():
    return ["USD", "EUR"]


@pytest.fixture
def seller(currencies):
    def _seller(
        external_id: str,  # Must be unique in Marketplace
        name="E2E Test Seller",
        currencies=currencies,
    ):
        return {
            "name": name,
            "address": {
                "addressLine1": "123 Main St",
                "city": "Anytown",
                "state": "CA",
                "postCode": "12345",
                "country": "US",
            },
            "currencies": currencies,
            "externalId": external_id,
        }

    return _seller


@pytest.fixture
def account():
    def _account(
        name: str = "Test Api Client Vendor",
    ):
        return {
            "name": name,
            "address": {
                "addressLine1": "123 Test St",
                "city": "San Francisco",
                "state": "CA",
                "postCode": "12345",
                "country": "US",
            },
            "type": "Vendor",
            "status": "Active",
        }

    return _account


@pytest.fixture
def api_token(account_id):
    def _api_token(
        name: str = "E2E Test API Token",
        description: str = "E2E API Token created during E2E tests",
    ):
        return {
            "account": {"id": account_id},
            "name": name,
            "description": description,
            "icon": "",
            "modules": [{"id": "MOD-1756"}],
        }

    return _api_token
