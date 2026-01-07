import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import (
    assert_async_service_filter_with_iterate,
    assert_async_update_resource,
    async_create_fixture_resource_and_delete,
)

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def async_price_lists_service(async_mpt_ops):
    return async_mpt_ops.catalog.price_lists


@pytest.fixture
async def async_created_price_list(async_price_lists_service, price_list_data):
    async with async_create_fixture_resource_and_delete(
        async_price_lists_service, price_list_data
    ) as price_list:
        yield price_list


def test_create_price_list(async_created_price_list, product_id):
    result = async_created_price_list

    assert result.product.id == product_id


async def test_get_price_list(async_price_lists_service, price_list_id):
    result = await async_price_lists_service.get(price_list_id)

    assert result.id == price_list_id


async def test_filter_price_lists(async_price_lists_service, price_list_id):
    await assert_async_service_filter_with_iterate(
        async_price_lists_service, price_list_id, ["-product"]
    )  # act


async def test_update_price_list(async_price_lists_service, price_list_id, short_uuid):
    await assert_async_update_resource(
        async_price_lists_service,
        price_list_id,
        "notes",
        f"Updated notes {short_uuid}",
    )  # act


async def test_delete_price_list(async_price_lists_service, async_created_price_list):
    await async_price_lists_service.delete(async_created_price_list.id)  # act


async def test_get_price_list_not_found(async_price_lists_service):
    bogus_id = "PRL-0000-NOTFOUND"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_price_lists_service.get(bogus_id)


async def test_create_price_list_invalid_data(async_price_lists_service):
    invalid_data = {"name": "e2e - delete me"}

    with pytest.raises(MPTAPIError, match=r"400 One or more validation errors occurred"):
        await async_price_lists_service.create(invalid_data)
