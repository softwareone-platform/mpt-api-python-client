import pytest


@pytest.fixture
def listing_id(e2e_config):
    return e2e_config["catalog.listing.id"]


@pytest.fixture
def listing_data(authorization_id, product_id, account_id, seller_id, price_list_id):
    return {
        "name": "e2e - please delete",
        "authorization": {
            "id": authorization_id,
        },
        "product": {
            "id": product_id,
        },
        "vendor": {
            "id": account_id,
        },
        "seller": {
            "id": seller_id,
        },
        "priceList": {"id": price_list_id},
        "primary": False,
        "notes": "",
        "eligibility": {"client": True, "partner": False},
    }
