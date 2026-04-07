import pytest

from tests.e2e.helper import (
    assert_async_service_filter_with_iterate,
    assert_async_update_resource,
)

pytestmark = [
    pytest.mark.flaky,
]


def test_async_create_category(async_created_category, category_data):
    result = async_created_category

    assert result.name == category_data["name"]


async def test_async_filter_categories(async_categories_service, async_category_id):
    await assert_async_service_filter_with_iterate(
        async_categories_service, async_category_id, None
    )  # act


async def test_async_update_category(async_categories_service, async_created_category, short_uuid):
    await assert_async_update_resource(
        async_categories_service,
        async_created_category.id,
        "name",
        f"e2e updated {short_uuid}",
    )


@pytest.mark.skip(reason="categories endpoint does not support delete in E2E environment")
async def test_async_delete_category(async_categories_service, async_created_category):
    await async_categories_service.delete(async_created_category.id)  # act
