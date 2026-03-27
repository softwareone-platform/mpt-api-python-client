import pytest


@pytest.fixture
def invalid_seller_id():
    return "SEL-0000-0000"


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
                "city": "Los Angeles",
                "state": "CA",
                "postCode": "12345",
                "country": "US",
            },
            "currencies": currencies,
            "externalId": external_id,
        }

    return _seller
