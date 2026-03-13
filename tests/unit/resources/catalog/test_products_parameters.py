import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.catalog.products_parameters import (
    AsyncParametersService,
    Parameter,
    ParametersService,
)


@pytest.fixture
def parameters_service(http_client):
    return ParametersService(http_client=http_client, endpoint_params={"product_id": "PRD-001"})


@pytest.fixture
def async_parameters_service(async_http_client):
    return AsyncParametersService(
        http_client=async_http_client, endpoint_params={"product_id": "PRD-001"}
    )


@pytest.fixture
def parameter_data():
    return {
        "id": "PRM-001",
        "name": "Tenant Name",
        "description": "The tenant name",
        "scope": "Agreement",
        "phase": "Configuration",
        "context": "Purchase",
        "type": "SingleLineText",
        "status": "Active",
        "externalId": "ext-001",
        "displayOrder": 1,
        "group": {"id": "GRP-001", "name": "General"},
        "product": {"id": "PRD-001", "name": "My Product"},
        "constraints": {"required": True, "hidden": False, "readonly": False},
        "audit": {
            "created": {"at": "2024-01-01T00:00:00Z"},
            "updated": {"at": "2024-01-02T00:00:00Z"},
        },
        "options": {"placeholder": "Enter tenant name"},
    }


def test_endpoint(parameters_service):
    result = parameters_service.path == "/public/v1/catalog/products/PRD-001/parameters"

    assert result is True


def test_async_endpoint(async_parameters_service):
    result = async_parameters_service.path == "/public/v1/catalog/products/PRD-001/parameters"

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "delete", "update", "iterate"])
def test_methods_present(parameters_service, method):
    result = hasattr(parameters_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "delete", "update", "iterate"])
def test_async_methods_present(async_parameters_service, method):
    result = hasattr(async_parameters_service, method)

    assert result is True


def test_parameter_primitive_fields(parameter_data):
    result = Parameter(parameter_data)

    assert result.to_dict() == parameter_data


def test_parameter_nested_fields_are_base_models(parameter_data):
    result = Parameter(parameter_data)

    assert isinstance(result.group, BaseModel)
    assert isinstance(result.product, BaseModel)
    assert isinstance(result.constraints, BaseModel)
    assert isinstance(result.audit, BaseModel)
    assert isinstance(result.options, BaseModel)


def test_parameter_nested_field_values(parameter_data):
    result = Parameter(parameter_data)

    assert result.group.id == "GRP-001"
    assert result.group.name == "General"
    assert result.product.id == "PRD-001"
    assert result.constraints.required is True
    assert result.constraints.hidden is False


def test_parameter_optional_fields_absent():
    result = Parameter({"id": "PRM-002"})

    assert result.id == "PRM-002"
    assert not hasattr(result, "name")
    assert not hasattr(result, "scope")
    assert not hasattr(result, "group")
    assert not hasattr(result, "options")
