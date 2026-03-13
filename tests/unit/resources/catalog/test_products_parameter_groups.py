import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.catalog.products_parameter_groups import (
    AsyncParameterGroupsService,
    ParameterGroup,
    ParameterGroupsService,
)


@pytest.fixture
def parameter_groups_service(http_client):
    return ParameterGroupsService(
        http_client=http_client, endpoint_params={"product_id": "PRD-001"}
    )


@pytest.fixture
def async_parameter_groups_service(async_http_client):
    return AsyncParameterGroupsService(
        http_client=async_http_client, endpoint_params={"product_id": "PRD-001"}
    )


@pytest.fixture
def parameter_group_data():
    return {
        "id": "GRP-001",
        "name": "General",
        "label": "General Settings",
        "description": "General configuration parameters",
        "displayOrder": 1,
        "default": True,
        "parameterCount": 5,
        "product": {"id": "PRD-001", "name": "My Product"},
        "audit": {
            "created": {"at": "2024-01-01T00:00:00Z"},
            "updated": {"at": "2024-01-02T00:00:00Z"},
        },
    }


def test_endpoint(parameter_groups_service):
    result = parameter_groups_service.path == "/public/v1/catalog/products/PRD-001/parameter-groups"

    assert result is True


def test_async_endpoint(async_parameter_groups_service):
    result = (
        async_parameter_groups_service.path
        == "/public/v1/catalog/products/PRD-001/parameter-groups"
    )

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "delete", "update", "iterate"])
def test_methods_present(parameter_groups_service, method):
    result = hasattr(parameter_groups_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "delete", "update", "iterate"])
def test_async_methods_present(async_parameter_groups_service, method):
    result = hasattr(async_parameter_groups_service, method)

    assert result is True


def test_parameter_group_primitive_fields(parameter_group_data):
    result = ParameterGroup(parameter_group_data)

    assert result.to_dict() == parameter_group_data


def test_parameter_group_nested_field_types(parameter_group_data):
    result = ParameterGroup(parameter_group_data)

    assert isinstance(result.product, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_parameter_group_nested_field_values(parameter_group_data):
    result = ParameterGroup(parameter_group_data)

    assert result.product.id == "PRD-001"
    assert result.product.name == "My Product"


def test_parameter_group_optional_fields_absent():
    result = ParameterGroup({"id": "GRP-002"})

    assert result.id == "GRP-002"
    assert not hasattr(result, "name")
    assert not hasattr(result, "label")
    assert not hasattr(result, "product")
    assert not hasattr(result, "audit")
