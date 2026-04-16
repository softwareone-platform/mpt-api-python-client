import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.program.programs_parameter_groups import (
    AsyncParameterGroupsService,
    ParameterGroup,
    ParameterGroupsService,
)


@pytest.fixture
def parameter_groups_service(http_client):
    return ParameterGroupsService(
        http_client=http_client, endpoint_params={"program_id": "PPG-001"}
    )


@pytest.fixture
def async_parameter_groups_service(async_http_client):
    return AsyncParameterGroupsService(
        http_client=async_http_client, endpoint_params={"program_id": "PPG-001"}
    )


@pytest.fixture
def parameter_group_data():
    return {
        "id": "GRP-001",
        "name": "Program Parameter Group",
        "label": "Program Parameter Group",
        "description": "Program Parameter Group",
        "displayOrder": 1,
        "default": True,
        "parameterCount": 5,
        "program": {"id": "PPG-001", "name": "Program"},
        "audit": {
            "created": {"at": "2024-01-01T00:00:00Z"},
            "updated": {"at": "2024-01-02T00:00:00Z"},
        },
    }


def test_endpoint(parameter_groups_service):
    result = parameter_groups_service.path == "/public/v1/program/programs/PPG-001/parameter-groups"

    assert result is True


def test_async_endpoint(async_parameter_groups_service):
    result = (
        async_parameter_groups_service.path
        == "/public/v1/program/programs/PPG-001/parameter-groups"
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

    assert isinstance(result.program, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_parameter_group_optional_fields_absent():
    result = ParameterGroup({"id": "PPG-001"})

    assert result.id == "PPG-001"
    assert not hasattr(result, "name")
    assert not hasattr(result, "label")
    assert not hasattr(result, "description")
    assert not hasattr(result, "program")
    assert not hasattr(result, "audit")
