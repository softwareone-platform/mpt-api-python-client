import pytest


@pytest.fixture
def invalid_buyer_id():
    return "BUY-0000-0000"


@pytest.fixture
def buyer_factory(client_account_id):
    def _buyer(
        name="E2E Created Buyer",
        account_id: str = client_account_id,
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
                "city": "Los Angeles",
                "state": "CA",
                "postCode": "12345",
                "country": "US",
            },
        }

    return _buyer
