import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import (
    assert_async_service_filter_with_iterate,
)

pytestmark = [pytest.mark.flaky]


async def test_get_price_list_item(async_price_list_items_service, price_list_item_id):
    result = await async_price_list_items_service.get(price_list_item_id)

    assert result.id == price_list_item_id


async def test_filter_price_list_items(async_price_list_items_service, price_list_item_id):
    await assert_async_service_filter_with_iterate(
        async_price_list_items_service, price_list_item_id, ["-notes"]
    )  # act


async def test_update_price_list_item(
    async_price_list_items_service, price_list_item_id, price_list_item_data
):
    result = await async_price_list_items_service.update(price_list_item_id, price_list_item_data)

    assert result.reason_for_change == price_list_item_data["reasonForChange"]


async def test_get_price_list_item_not_found(async_price_list_items_service):
    bogus_id = "PRI-0000-NOTFOUND"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_price_list_items_service.get(bogus_id)


async def test_update_price_list_item_invalid_data(
    async_price_list_items_service, price_list_item_id
):
    invalid_data = {"unitPP": "NaN"}

    with pytest.raises(MPTAPIError, match=r"400 Bad Request"):
        await async_price_list_items_service.update(price_list_item_id, invalid_data)
