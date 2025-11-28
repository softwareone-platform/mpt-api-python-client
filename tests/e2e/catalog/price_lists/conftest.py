import pytest


@pytest.fixture
def price_list_data(product_id):
    return {
        "notes": "e2e - price list please delete",
        "defaultMarkup": "20.0",
        "product": {"id": product_id},
        "currency": "USD",
        "default": False,
    }


@pytest.fixture
def price_lists_service(mpt_ops):
    return mpt_ops.catalog.price_lists


@pytest.fixture
def price_list_id(created_price_list):
    return created_price_list.id
