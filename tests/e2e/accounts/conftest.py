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
def seller_factory(currencies):
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
def account_factory():
    def _account(
        name: str = "E2E Test Api Client Vendor",
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
def buyer_factory(buyer_account_id):
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
def user_group_factory(account_id, module_id):
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
def api_token_factory(account_id, module_id):
    def _api_token(
        name: str = "E2E Test API Token",
        description: str = "E2E API Token created during E2E tests",
    ):
        return {
            "account": {"id": account_id},
            "name": name,
            "description": description,
            "icon": "",
            "modules": [{"id": module_id}],
        }

    return _api_token


@pytest.fixture
def licensee_factory(seller_id, buyer_id, user_group_factory, licensee_account_id):
    def _licensee(
        name: str = "Test E2E Licensee",
        licensee_type: str = "Client",
    ):
        group = user_group_factory(user_group_account_id=licensee_account_id)

        return {
            "name": name,
            "address": {
                "addressLine1": "456 Licensee St",
                "city": "Los Angeles",
                "state": "CA",
                "postCode": "67890",
                "country": "US",
            },
            "useBuyerAddress": False,
            "seller": {"id": seller_id},
            "buyer": {"id": buyer_id},
            "account": {"id": licensee_account_id},
            "eligibility": {"client": True, "partner": False},
            "groups": [group],
            "type": licensee_type,
            "status": "Enabled",
            "defaultLanguage": "en-US",
        }

    return _licensee
