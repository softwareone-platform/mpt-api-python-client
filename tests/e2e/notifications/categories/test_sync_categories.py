import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_category(mpt_ops, category_data):
    service = mpt_ops.notifications.categories
    category = service.create(category_data)
    yield category
    try:
        service.delete(category.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete category {category.id}: {error.title}")  # noqa: WPS421


def test_create_category(created_category, category_data):
    assert created_category.name == category_data["name"]  # act

    assert created_category.description == category_data["description"]


def test_get_category(mpt_client, category_id):
    service = mpt_client.notifications.categories

    result = service.get(category_id)

    assert result.id == category_id


@pytest.mark.skip(reason="created_category kills performance due to MPT-13785")
def test_update_category(mpt_ops, created_category):
    service = mpt_ops.notifications.categories
    update_data = {
        "name": "e2e-updated-category",
        "description": "Updated description",
    }

    result = service.update(created_category.id, update_data)

    assert result.name == "e2e-updated-category"
    assert result.description == "Updated description"



def test_filter_categories(mpt_client, category_id):
    service = mpt_client.notifications.categories

    result = list(service.filter(RQLQuery(id=category_id)).iterate())

    assert len(result) == 1
    assert result[0].id == category_id


@pytest.mark.skip(reason="created_category kills performance due to MPT-13785")
def test_publish_category(mpt_ops, created_category):
    service = mpt_ops.notifications.categories
    unpublish_note_data = {"note": "Unpublishing category for testing"}
    service.unpublish(created_category.id, unpublish_note_data)
    note_data = {"note": "Publishing category for testing"}

    result = service.publish(created_category.id, note_data)

    assert result.id == created_category.id


@pytest.mark.skip(reason="created_category kills performance due to MPT-13785")
def test_unpublish_category(mpt_ops, created_category):
    service = mpt_ops.notifications.categories
    unpublish_note_data = {"note": "Unpublishing category for testing"}

    result = service.unpublish(created_category.id, unpublish_note_data)

    assert result.id == created_category.id


def test_category_not_found(mpt_client, invalid_category_id):
    service = mpt_client.notifications.categories

    with pytest.raises(MPTAPIError):
        service.get(invalid_category_id)


def test_delete_category(mpt_ops, created_category):
    service = mpt_ops.notifications.categories

    service.delete(created_category.id)  # act


def test_delete_category_not_found(mpt_ops, invalid_category_id):
    service = mpt_ops.notifications.categories

    with pytest.raises(MPTAPIError):
        service.delete(invalid_category_id)
