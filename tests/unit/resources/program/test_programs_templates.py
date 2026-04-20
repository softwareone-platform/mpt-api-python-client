import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.program.programs_templates import (
    AsyncTemplatesService,
    Template,
    TemplatesService,
)


@pytest.fixture
def templates_service(http_client):
    return TemplatesService(http_client=http_client, endpoint_params={"program_id": "PTM-001"})


@pytest.fixture
def async_templates_service(async_http_client):
    return AsyncTemplatesService(
        http_client=async_http_client, endpoint_params={"program_id": "PTM-001"}
    )


@pytest.fixture
def template_data():
    return {
        "id": "TPL-001",
        "name": "Program Template",
        "content": "<p>Template Content</p>",
        "default": True,
        "externalIds": {"vendor": "EXT-001"},
        "type": "Email",
        "status": "Active",
        "program": {"id": "PTM-001", "name": "Program"},
        "audit": {
            "created": {"at": "2024-01-01T00:00:00Z"},
            "updated": {"at": "2024-01-02T00:00:00Z"},
        },
    }


def test_endpoint(templates_service):
    result = templates_service.path == "/public/v1/program/programs/PTM-001/templates"

    assert result is True


def test_async_endpoint(async_templates_service):
    result = async_templates_service.path == "/public/v1/program/programs/PTM-001/templates"

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "delete", "update", "iterate"])
def test_methods_present(templates_service, method):
    result = hasattr(templates_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "delete", "update", "iterate"])
def test_async_methods_present(async_templates_service, method):
    result = hasattr(async_templates_service, method)

    assert result is True


def test_template_primitive_fields(template_data):
    result = Template(template_data)

    assert result.to_dict() == template_data


def test_template_nested_field_types(template_data):
    result = Template(template_data)

    assert isinstance(result.external_ids, BaseModel)
    assert isinstance(result.program, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_template_optional_fields_absent():
    result = Template({"id": "TPL-001"})

    assert result.id == "TPL-001"
    assert not hasattr(result, "name")
    assert not hasattr(result, "content")
    assert not hasattr(result, "default")
    assert not hasattr(result, "external_ids")
    assert not hasattr(result, "type")
    assert not hasattr(result, "status")
    assert not hasattr(result, "program")
    assert not hasattr(result, "audit")
