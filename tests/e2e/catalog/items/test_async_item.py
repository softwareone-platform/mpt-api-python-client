import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def async_created_item(logger, async_mpt_vendor, item_data):
    service = async_mpt_vendor.catalog.items
    item = await service.create(item_data)
    yield item
    try:
        await service.delete(item.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete item {item.id}: {error.title}")  # noqa: WPS421


def test_create_item(async_created_item):
    result = async_created_item.name == "e2e - please delete"

    assert result is True


async def test_update_item(async_mpt_vendor, async_created_item):
    service = async_mpt_vendor.catalog.items
    update_data = {"name": "e2e - delete me (updated)"}

    result = await service.update(async_created_item.id, update_data)

    assert result.name == "e2e - delete me (updated)"


@pytest.mark.skip(reason="Leaves test items in the catalog")
async def test_review_and_publish_item(async_mpt_vendor, async_mpt_ops, async_created_item):
    item = await async_mpt_vendor.catalog.items.review(async_created_item.id)
    assert item.status == "Pending"

    item = await async_mpt_ops.catalog.items.publish(async_created_item.id)
    assert item.status == "Published"


async def test_get_item(async_mpt_vendor, item_id):
    service = async_mpt_vendor.catalog.items

    result = await service.get(item_id)

    assert result.id == item_id


async def test_iterate_items(async_mpt_vendor, async_created_item):
    service = async_mpt_vendor.catalog.items
    items = [item async for item in service.iterate()]

    result = any(item.id == async_created_item.id for item in items)

    assert result is True


async def test_filter(async_mpt_vendor, item_id):
    service = async_mpt_vendor.catalog.items

    result = [item async for item in service.filter(RQLQuery(id=item_id)).iterate()]

    assert len(result) == 1
    assert result[0].id == item_id


async def test_not_found(async_mpt_vendor):
    service = async_mpt_vendor.catalog.items

    with pytest.raises(MPTAPIError):
        await service.get("ITM-000-000")


async def test_delete_item(async_mpt_vendor, async_created_item):
    service = async_mpt_vendor.catalog.items

    await service.delete(async_created_item.id)  # act

    with pytest.raises(MPTAPIError):
        await service.get(async_created_item.id)
