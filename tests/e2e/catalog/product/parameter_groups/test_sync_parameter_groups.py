import pytest

from mpt_api_client.exceptions import MPTAPIError


@pytest.fixture
def created_parameter_group(logger, mpt_vendor, product_id, parameter_group_data):
    service = mpt_vendor.catalog.products.parameter_groups(product_id)
    group = service.create(parameter_group_data)
    yield group
    try:
        service.delete(group.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete parameter group {group.id}: {error.title}")  # noqa: WPS421


@pytest.mark.flaky
def test_create_parameter_group(created_parameter_group):
    result = created_parameter_group.name == "e2e - please delete"

    assert result is True


@pytest.mark.flaky
def test_update_parameter_group(mpt_vendor, product_id, created_parameter_group):
    service = mpt_vendor.catalog.products.parameter_groups(product_id)
    update_data = {"name": "please delete me"}

    result = service.update(created_parameter_group.id, update_data)

    assert result.name == "please delete me"


@pytest.mark.flaky
def test_get_parameter_group_get(mpt_vendor, product_id, parameter_group_id):
    service = mpt_vendor.catalog.products.parameter_groups(product_id)

    result = service.get(parameter_group_id)

    assert result.id == parameter_group_id


@pytest.mark.flaky
def test_iterate_parameter_groups(mpt_vendor, product_id, created_parameter_group):
    service = mpt_vendor.catalog.products.parameter_groups(product_id)
    groups = list(service.iterate())

    result = any(group.id == created_parameter_group.id for group in groups)

    assert result is True


@pytest.mark.flaky
def test_delete_parameter_group(mpt_vendor, product_id, created_parameter_group):
    service = mpt_vendor.catalog.products.parameter_groups(product_id)

    service.delete(created_parameter_group.id)  # act

    with pytest.raises(MPTAPIError):
        service.get(created_parameter_group.id)
