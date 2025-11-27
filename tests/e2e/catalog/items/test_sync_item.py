import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_item(mpt_vendor, item_data):
    service = mpt_vendor.catalog.items
    item = service.create(item_data)
    yield item
    try:
        service.delete(item.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete item {item.id}: {error.title}")  # noqa: WPS421


def test_create_item(created_item):
    result = created_item.name == "e2e - please delete"

    assert result is True


def test_update_item(mpt_vendor, created_item):
    service = mpt_vendor.catalog.items
    update_data = {"name": "please delete me"}

    result = service.update(created_item.id, update_data)

    assert result.name == "please delete me"


@pytest.mark.skip(reason="Leaves test items in the catalog")  # noqa: AAA01
def test_review_and_publish_item(mpt_vendor, mpt_ops, created_item):
    item = mpt_vendor.catalog.items.review(created_item.id)
    assert item.status == "Pending"

    item = mpt_ops.catalog.items.publish(created_item.id)
    assert item.status == "Published"


def test_get_item(mpt_vendor, item_id):
    service = mpt_vendor.catalog.items

    result = service.get(item_id)

    assert result.id == item_id


def test_iterate_items(mpt_vendor, created_item):
    service = mpt_vendor.catalog.items
    items = list(service.iterate())

    result = any(item.id == created_item.id for item in items)

    assert result is True


def test_filter(mpt_vendor, item_id):
    service = mpt_vendor.catalog.items

    result = list(service.filter(RQLQuery(id=item_id)).iterate())

    assert len(result) == 1
    assert result[0].id == item_id


def test_not_found(mpt_vendor):
    service = mpt_vendor.catalog.items

    with pytest.raises(MPTAPIError):
        service.get("ITM-000-000")


def test_delete_item(mpt_vendor, created_item):
    service = mpt_vendor.catalog.items

    service.delete(created_item.id)  # act

    with pytest.raises(MPTAPIError):
        service.get(created_item.id)
