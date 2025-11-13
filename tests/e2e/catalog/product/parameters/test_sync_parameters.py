import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_parameter(mpt_vendor, product_id, parameter_data):
    service = mpt_vendor.catalog.products.parameters(product_id)
    parameter = service.create(parameter_data)
    yield parameter
    try:
        service.delete(parameter.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete parameter {parameter.id}: {error.title}")


def test_create_parameter(created_parameter):
    assert created_parameter.name == "e2e - please delete"


def test_create_parameter_wrong_data(mpt_vendor, product_id):
    parameter_data = {"name": "e2e - please delete - wrong data test"}
    service = mpt_vendor.catalog.products.parameters(product_id)
    with pytest.raises(MPTAPIError):
        service.create(
            parameter_data,
        )


def test_update_parameter(mpt_vendor, product_id, created_parameter):
    service = mpt_vendor.catalog.products.parameters(product_id)
    update_data = {"name": "please delete me"}
    parameter = service.update(created_parameter.id, update_data)
    assert parameter.name == "please delete me"


def test_get_parameter(mpt_vendor, product_id, parameter_id):
    service = mpt_vendor.catalog.products.parameters(product_id)
    parameter = service.get(parameter_id)
    assert parameter.id == parameter_id


def test_iterate_parameters(mpt_vendor, product_id, created_parameter):
    service = mpt_vendor.catalog.products.parameters(product_id)
    product_parameters = list(service.iterate())
    assert any(parameter.id == created_parameter.id for parameter in product_parameters)


def test_delete_parameter(mpt_vendor, product_id, created_parameter):
    service = mpt_vendor.catalog.products.parameters(product_id)
    service.delete(created_parameter.id)

    parameter = service.get(created_parameter.id)
    assert parameter.status == "Deleted"
