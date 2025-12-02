import pytest


@pytest.fixture
def price_list_items_service(mpt_ops, price_list_id):
    return mpt_ops.catalog.price_lists.items(price_list_id)


@pytest.fixture
def async_price_list_items_service(async_mpt_ops, price_list_id):
    return async_mpt_ops.catalog.price_lists.items(price_list_id)


@pytest.fixture
def price_list_item_data(short_uuid):
    return {
        "reasonForChange": f"Updated {short_uuid}",
        "unitPP": 10,
        "unitLP": 10,
    }


@pytest.fixture
def price_list_item(price_list_items_service):
    price_list_items = price_list_items_service.fetch_page(1)
    return price_list_items[0]
