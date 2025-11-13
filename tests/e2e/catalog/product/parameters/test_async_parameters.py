import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def async_created_parameter(async_mpt_vendor, product_id, parameter_data):
    service = async_mpt_vendor.catalog.products.parameters(product_id)
    parameter = await service.create(parameter_data)
    yield parameter
    try:
        await service.delete(parameter.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete parameter {parameter.id}: {error.title}")


def test_create_parameter(async_created_parameter):
    assert async_created_parameter.name == "e2e - please delete"


async def test_create_parameter_wrong_data(async_mpt_vendor, product_id):
    parameter_data = {"name": "e2e - please delete - wrong data test"}
    service = async_mpt_vendor.catalog.products.parameters(product_id)
    with pytest.raises(MPTAPIError):
        await service.create(parameter_data)


async def test_update_parameter(async_mpt_vendor, product_id, async_created_parameter):
    service = async_mpt_vendor.catalog.products.parameters(product_id)
    update_data = {"name": "please delete me"}
    parameter = await service.update(async_created_parameter.id, update_data)
    assert parameter.name == "please delete me"


async def test_get_parameter(async_mpt_vendor, product_id, parameter_id):
    service = async_mpt_vendor.catalog.products.parameters(product_id)
    parameter = await service.get(parameter_id)
    assert parameter.id == parameter_id


async def test_iterate_parameters(async_mpt_vendor, product_id, async_created_parameter):
    service = async_mpt_vendor.catalog.products.parameters(product_id)
    product_parameters = [product_param async for product_param in service.iterate()]
    assert any(parameter.id == async_created_parameter.id for parameter in product_parameters)


async def test_delete_parameter(async_mpt_vendor, product_id, async_created_parameter):
    service = async_mpt_vendor.catalog.products.parameters(product_id)
    await service.delete(async_created_parameter.id)
    parameter = await service.get(async_created_parameter.id)
    assert parameter.status == "Deleted"
