import pytest

from tests.e2e.helper import create_fixture_resource_and_delete


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
def created_price_list(price_lists_service, price_list_data):
    with create_fixture_resource_and_delete(price_lists_service, price_list_data) as price_list:
        yield price_list


@pytest.fixture
def price_list_id(e2e_config):
    return e2e_config["catalog.price_list.id"]
