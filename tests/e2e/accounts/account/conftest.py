import pytest


@pytest.fixture
def invalid_account_id():
    return "ACC-0000-0000"


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
