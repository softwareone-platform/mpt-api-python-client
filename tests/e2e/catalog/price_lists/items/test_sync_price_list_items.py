import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import (
    assert_service_filter_with_iterate,
)

pytestmark = [pytest.mark.flaky]


def test_get_price_list_item(price_list_items_service, price_list_item_id):
    result = price_list_items_service.get(price_list_item_id)

    assert result.id == price_list_item_id


def test_filter_price_list_items(price_list_items_service, price_list_item_id):
    assert_service_filter_with_iterate(
        price_list_items_service, price_list_item_id, ["-notes"]
    )  # act


def test_update_price_list_item(price_list_items_service, price_list_item_id, price_list_item_data):
    result = price_list_items_service.update(price_list_item_id, price_list_item_data)

    assert result.reason_for_change == price_list_item_data["reasonForChange"]


def test_get_price_list_item_not_found(price_list_items_service):
    bogus_id = "PRI-0000-NOTFOUND"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        price_list_items_service.get(bogus_id)


def test_update_price_list_item_invalid_data(price_list_items_service, price_list_item_id):
    invalid_data = {"unitPP": "NaN"}

    with pytest.raises(MPTAPIError, match=r"400 Bad Request"):
        price_list_items_service.update(price_list_item_id, invalid_data)
