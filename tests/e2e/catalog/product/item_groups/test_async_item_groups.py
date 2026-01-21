import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery  # added import

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def async_created_item_group(async_mpt_vendor, product_id, item_group_data):
    service = async_mpt_vendor.catalog.products.item_groups(product_id)
    group = await service.create(item_group_data)
    yield group
    try:
        await service.delete(group.id)
    except MPTAPIError as error:  # noqa: WPS421
        print(f"TEARDOWN - Unable to delete item group {group.id}: {error.title}")


def test_create_item_group(async_created_item_group):
    result = async_created_item_group.name == "e2e - please delete"

    assert result is True


async def test_update_item_group(async_mpt_vendor, product_id, async_created_item_group):
    service = async_mpt_vendor.catalog.products.item_groups(product_id)
    update_data = {"name": "e2e - delete me (updated)"}

    result = await service.update(async_created_item_group.id, update_data)

    assert result.name == "e2e - delete me (updated)"


async def test_get_item_group(async_mpt_vendor, product_id, item_group_id):
    service = async_mpt_vendor.catalog.products.item_groups(product_id)

    result = await service.get(item_group_id)

    assert result.id == item_group_id


async def test_get_item_group_by_id(async_mpt_vendor, product_id, item_group_id):
    service = async_mpt_vendor.catalog.products.item_groups(product_id)

    result = await service.get(item_group_id)

    assert result.id == item_group_id


async def test_iterate_item_groups(async_mpt_vendor, product_id, async_created_item_group):
    service = async_mpt_vendor.catalog.products.item_groups(product_id)
    groups = [group async for group in service.iterate()]

    result = any(group.id == async_created_item_group.id for group in groups)

    assert result is True


async def test_filter_item_groups(async_mpt_vendor, product_id, item_group_id):
    select_fields = ["-description"]
    filtered_item_groups = (
        async_mpt_vendor.catalog.products
        .item_groups(product_id)
        .filter(RQLQuery(id=item_group_id))
        .select(*select_fields)
    )

    result = [group async for group in filtered_item_groups.iterate()]

    assert len(result) == 1
    assert result[0].id == item_group_id


async def test_delete_item_group(async_mpt_vendor, product_id, async_created_item_group):
    service = async_mpt_vendor.catalog.products.item_groups(product_id)

    await service.delete(async_created_item_group.id)  # act

    with pytest.raises(MPTAPIError):
        await service.get(async_created_item_group.id)
