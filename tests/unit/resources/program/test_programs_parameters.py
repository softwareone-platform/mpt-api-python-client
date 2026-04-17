import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.program.programs_parameters import (
    AsyncParametersService,
    Parameter,
    ParametersService,
)


@pytest.fixture
def parameters_service(http_client):
    return ParametersService(http_client=http_client, endpoint_params={"program_id": "PPM-001"})


@pytest.fixture
def async_parameters_service(async_http_client):
    return AsyncParametersService(
        http_client=async_http_client, endpoint_params={"program_id": "PPM-001"}
    )


@pytest.fixture
def parameter_data():
    return {
        "id": "PRM-001",
        "name": "Program Parameter",
        "scope": "Enrollment",
        "phase": "Fulfillment",
        "program": {"id": "PPM-001", "name": "My Program"},
        "description": "Program Parameter",
        "multiple": False,
        "externalId": "ext-001",
        "displayOrder": 1,
        "constraints": {"required": True, "hidden": False, "readonly": False},
        "options": {"placeholder": "Program Parameter"},
        "type": "SingleLineText",
        "status": "Active",
        "audit": {
            "created": {"at": "2024-01-01T00:00:00Z"},
            "updated": {"at": "2024-01-02T00:00:00Z"},
        },
    }


def test_endpoint(parameters_service):
    result = parameters_service.path == "/public/v1/program/programs/PPM-001/parameters"

    assert result is True


def test_async_endpoint(async_parameters_service):
    result = async_parameters_service.path == "/public/v1/program/programs/PPM-001/parameters"

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "delete", "update", "iterate"])
def test_methods_present(parameters_service, method):
    result = hasattr(parameters_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "delete", "update", "iterate"])
def test_async_methods_present(async_parameters_service, method):
    result = hasattr(async_parameters_service, method)

    assert result is True


def test_template_primitive_fields(parameter_data):
    result = Parameter(parameter_data)

    assert result.to_dict() == parameter_data


def test_template_nested_field_types(parameter_data):
    result = Parameter(parameter_data)

    assert isinstance(result.program, BaseModel)
    assert isinstance(result.constraints, BaseModel)
    assert isinstance(result.options, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_template_optional_fields_absent():
    result = Parameter({"id": "PRM-001"})

    assert result.id == "PRM-001"
    assert not hasattr(result, "name")
    assert not hasattr(result, "scope")
    assert not hasattr(result, "phase")
    assert not hasattr(result, "program")
    assert not hasattr(result, "description")
    assert not hasattr(result, "multiple")
    assert not hasattr(result, "external_id")
    assert not hasattr(result, "display_order")
    assert not hasattr(result, "constraints")
    assert not hasattr(result, "options")
    assert not hasattr(result, "type")
    assert not hasattr(result, "status")
    assert not hasattr(result, "audit")
