import pytest

from tests.e2e.helper import (
    async_create_fixture_resource_and_delete,
    create_fixture_resource_and_delete,
)


@pytest.fixture
def categories_service(mpt_ops):
    return mpt_ops.integration.categories


@pytest.fixture
def async_categories_service(async_mpt_ops):
    return async_mpt_ops.integration.categories


@pytest.fixture
def category_data(short_uuid):
    return {
        "name": f"e2e - please delete {short_uuid}",
        "description": "Created by automated E2E tests. Safe to delete.",
    }


@pytest.fixture
def created_category(categories_service, category_data):
    with create_fixture_resource_and_delete(categories_service, category_data) as category:
        yield category


@pytest.fixture
async def async_created_category(async_categories_service, category_data):
    async with async_create_fixture_resource_and_delete(
        async_categories_service, category_data
    ) as category:
        yield category


@pytest.fixture
def category_id(created_category):
    return created_category.id


@pytest.fixture
def async_category_id(async_created_category):
    return async_created_category.id
