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
def buyer(buyer_account_id):
    def _buyer(
        name="E2E Created Buyer",
        account_id: str = buyer_account_id,
    ):
        return {
            "name": name,
            "account": {
                "id": account_id,
            },
            "contact": {
                "firstName": "first",
                "lastName": "last",
                "email": "created.buyer@example.com",
            },
            "address": {
                "addressLine1": "123 Main St",
                "city": "Anytown",
                "state": "CA",
                "postCode": "12345",
                "country": "US",
            },
        }

    return _buyer


@pytest.fixture
def licensee(seller_id, seller, buyer_id, buyer, account_id, account):
    def _licensee(
        name: str = "Test E2E Licensee",
    ):
        seller_data = seller(external_id="E2E Seeded Seller")
        buyer_data = buyer(external_id="E2E Seeded Buyer")
        account_data = account(name="E2E Seeded Account")

        licensee_seller_data = {"id": seller_id, **seller_data}
        licensee_buyer_data = {"id": buyer_id, **buyer_data}
        licensee_account_data = {"id": account_id, **account_data}

        return {
            "name": name,
            "address": {
                "addressLine1": "456 Licensee St",
                "city": "Los Angeles",
                "state": "CA",
                "postCode": "67890",
                "country": "US",
            },
            "useBuyerAddress": True,
            "seller": licensee_seller_data,
            "buyer": licensee_buyer_data,
            "account": licensee_account_data,
            "eligibility": {
                "client": True,
                "partner": False
            },
        }

    return _licensee
