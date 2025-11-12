import pytest

from mpt_api_client.exceptions import MPTAPIError


@pytest.fixture
async def async_created_parameter_group(logger, async_mpt_vendor, product_id, parameter_group_data):
    service = async_mpt_vendor.catalog.products.parameter_groups(product_id)
    group = await service.create(parameter_group_data)
    yield group
    try:
        await service.delete(group.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete parameter group {group.id}: {error.title}")  # noqa: WPS421


@pytest.mark.flaky
def test_create_parameter_group(async_created_parameter_group):
    assert async_created_parameter_group.name == "e2e - please delete"


@pytest.mark.flaky
async def test_update_parameter_group(async_mpt_vendor, product_id, async_created_parameter_group):
    service = async_mpt_vendor.catalog.products.parameter_groups(product_id)
    update_data = {"name": "e2e - delete me (updated)"}
    group = await service.update(async_created_parameter_group.id, update_data)
    assert group.name == "e2e - delete me (updated)"


@pytest.mark.flaky
async def test_get_parameter_group(async_mpt_vendor, product_id, parameter_group_id):
    service = async_mpt_vendor.catalog.products.parameter_groups(product_id)
    group = await service.get(parameter_group_id)
    assert group.id == parameter_group_id


@pytest.mark.flaky
async def test_iterate_parameter_groups(
    async_mpt_vendor, product_id, async_created_parameter_group
):
    service = async_mpt_vendor.catalog.products.parameter_groups(product_id)
    groups = [group async for group in service.iterate()]
    assert any(group.id == async_created_parameter_group.id for group in groups)


@pytest.mark.flaky
async def test_delete_parameter_group(async_mpt_vendor, product_id, async_created_parameter_group):
    service = async_mpt_vendor.catalog.products.parameter_groups(product_id)
    await service.delete(async_created_parameter_group.id)
    with pytest.raises(MPTAPIError):
        await service.get(async_created_parameter_group.id)
