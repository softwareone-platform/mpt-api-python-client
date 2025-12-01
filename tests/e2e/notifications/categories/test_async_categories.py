import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def async_created_category(async_mpt_ops, category_data):
    service = async_mpt_ops.notifications.categories
    category = await service.create(category_data)
    yield category
    try:
        await service.delete(category.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete category {category.id}: {error.title}")  # noqa: WPS421


@pytest.mark.skip(reason="async_created_category kills performance due to MPT-13785")  # noqa: AAA01
def test_create_category(async_created_category, category_data):
    assert async_created_category.name == category_data["name"]
    assert async_created_category.description == category_data["description"]


@pytest.mark.skip(reason="async_created_category kills performance due to MPT-13785")
async def test_get_category(async_mpt_vendor, async_created_category):
    service = async_mpt_vendor.notifications.categories

    result = await service.get(async_created_category.id)

    assert result.id == async_created_category.id
    assert result.name == async_created_category.name


@pytest.mark.skip(reason="async_created_category kills performance due to MPT-13785")
async def test_update_category(async_mpt_ops, async_created_category):
    service = async_mpt_ops.notifications.categories
    update_data = {
        "name": "e2e-async-updated-category",
        "description": "Async updated description",
    }

    result = await service.update(async_created_category.id, update_data)

    assert result.name == "e2e-async-updated-category"
    assert result.description == "Async updated description"


@pytest.mark.skip(reason="async_created_category kills performance due to MPT-13785")
async def test_list_categories(async_mpt_vendor, async_created_category):
    service = async_mpt_vendor.notifications.categories

    result = [category async for category in service.iterate()]

    assert any(category.id == async_created_category.id for category in result)


@pytest.mark.skip(reason="async_created_category kills performance due to MPT-13785")
async def test_filter_categories(async_mpt_vendor, async_created_category):
    service = async_mpt_vendor.notifications.categories

    result = [
        category
        async for category in service.filter(RQLQuery(id=async_created_category.id)).iterate()
    ]

    assert len(result) == 1
    assert result[0].id == async_created_category.id


@pytest.mark.skip(reason="async_created_category kills performance due to MPT-13785")
async def test_publish_category(async_mpt_ops, async_created_category):
    service = async_mpt_ops.notifications.categories
    unpublish_note_data = {"note": "Unpublishing category for async testing"}
    await service.unpublish(async_created_category.id, unpublish_note_data)
    note_data = {"note": "Publishing category for async testing"}

    result = await service.publish(async_created_category.id, note_data)

    assert result.id == async_created_category.id


@pytest.mark.skip(reason="async_created_category kills performance due to MPT-13785")
async def test_unpublish_category(async_mpt_ops, async_created_category):
    service = async_mpt_ops.notifications.categories
    unpublish_note_data = {"note": "Unpublishing category for async testing"}

    result = await service.unpublish(async_created_category.id, unpublish_note_data)

    assert result.id == async_created_category.id


async def test_category_not_found(async_mpt_vendor, invalid_category_id):
    service = async_mpt_vendor.notifications.categories

    with pytest.raises(MPTAPIError):
        await service.get(invalid_category_id)


@pytest.mark.skip(reason="async_created_category kills performance due to MPT-13785")
async def test_delete_category(async_mpt_ops, async_created_category):
    service = async_mpt_ops.notifications.categories

    await service.delete(async_created_category.id)

    with pytest.raises(MPTAPIError):
        await service.get(async_created_category.id)


async def test_delete_category_not_found(async_mpt_ops, invalid_category_id):
    service = async_mpt_ops.notifications.categories

    with pytest.raises(MPTAPIError):
        await service.delete(invalid_category_id)
