import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery  # added import

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_item_group(mpt_vendor, product_id, item_group_data):
    service = mpt_vendor.catalog.products.item_groups(product_id)
    group = service.create(item_group_data)
    yield group
    try:
        service.delete(group.id)
    except MPTAPIError as error:  # noqa: WPS421
        print(f"TEARDOWN - Unable to delete item group {group.id}: {error.title}")


def test_create_item_group(created_item_group):
    result = created_item_group.name == "e2e - please delete"

    assert result is True


def test_update_item_group(mpt_vendor, product_id, created_item_group):
    service = mpt_vendor.catalog.products.item_groups(product_id)
    update_data = {"name": "please delete me"}

    result = service.update(created_item_group.id, update_data)

    assert result.name == "please delete me"


def test_get_item_group(mpt_vendor, product_id, created_item_group):
    service = mpt_vendor.catalog.products.item_groups(product_id)

    result = service.get(created_item_group.id)

    assert result.id == created_item_group.id


def test_get_item_group_by_id(mpt_vendor, product_id, item_group_id):
    service = mpt_vendor.catalog.products.item_groups(product_id)

    result = service.get(item_group_id)

    assert result.id == item_group_id


def test_iterate_item_groups(mpt_vendor, product_id, created_item_group):
    service = mpt_vendor.catalog.products.item_groups(product_id)
    groups = list(service.iterate())

    result = any(group.id == created_item_group.id for group in groups)

    assert result is True


def test_filter_item_groups(mpt_vendor, product_id, item_group_id):
    select_fields = ["-description"]
    filtered_item_groups = (
        mpt_vendor.catalog.products
        .item_groups(product_id)
        .filter(RQLQuery(id=item_group_id))
        .select(*select_fields)
    )

    result = list(filtered_item_groups.iterate())

    assert len(result) == 1
    assert result[0].id == item_group_id


def test_delete_item_group(mpt_vendor, product_id, created_item_group):
    service = mpt_vendor.catalog.products.item_groups(product_id)

    service.delete(created_item_group.id)  # act

    with pytest.raises(MPTAPIError):
        service.get(created_item_group.id)
