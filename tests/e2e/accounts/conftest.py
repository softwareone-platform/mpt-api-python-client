import datetime as dt
import pathlib

import pytest


@pytest.fixture(scope="session")
def timestamp():
    return int(dt.datetime.now(tz=dt.UTC).strftime("%Y%m%d%H%M%S"))


@pytest.fixture
def account_data():
    return {
        "name": "Test Api Client Vendor",
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


@pytest.fixture
def account_icon():
    return pathlib.Path(__file__).parent / "logo.png"


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
