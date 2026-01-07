import pytest

from mpt_api_client import RQLQuery


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
def price_list_item(price_list_items_service, item_id):
    return next(price_list_items_service.filter(RQLQuery(item__id=item_id)).iterate())


@pytest.fixture
def price_list_item_id(price_list_item):
    return price_list_item.id
