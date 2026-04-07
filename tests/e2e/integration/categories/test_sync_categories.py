import pytest

from tests.e2e.helper import assert_service_filter_with_iterate, assert_update_resource

pytestmark = [
    pytest.mark.flaky,
]


def test_create_category(created_category, category_data):
    result = created_category

    assert result.name == category_data["name"]


def test_filter_categories(categories_service, category_id):
    assert_service_filter_with_iterate(categories_service, category_id, None)  # act


def test_update_category(categories_service, created_category, short_uuid):
    assert_update_resource(
        categories_service,
        created_category.id,
        "name",
        f"e2e updated {short_uuid}",
    )  # act


@pytest.mark.skip(reason="categories endpoint does not support delete in E2E environment")
def test_delete_category(categories_service, created_category):
    categories_service.delete(created_category.id)  # act
