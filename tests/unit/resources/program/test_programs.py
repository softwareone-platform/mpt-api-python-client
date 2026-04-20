import httpx
import pytest
import respx

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.program.programs import AsyncProgramsService, Program, ProgramsService
from mpt_api_client.resources.program.programs_documents import (
    AsyncDocumentService,
    DocumentService,
)
from mpt_api_client.resources.program.programs_media import (
    AsyncMediaService,
    MediaService,
)
from mpt_api_client.resources.program.programs_parameter_groups import (
    AsyncParameterGroupsService,
    ParameterGroupsService,
)
from mpt_api_client.resources.program.programs_parameters import (
    AsyncParametersService,
    ParametersService,
)
from mpt_api_client.resources.program.programs_templates import (
    AsyncTemplatesService,
    TemplatesService,
)


@pytest.fixture
def programs_service(http_client):
    return ProgramsService(http_client=http_client)


@pytest.fixture
def async_programs_service(async_http_client):
    return AsyncProgramsService(http_client=async_http_client)


@pytest.fixture
def program_settings_data():
    return {"settingKey": "setting_value"}


@pytest.fixture
def program_data(program_settings_data):
    return {
        "id": "PRG-123",
        "name": "Test Program",
        "website": "https://example.com",
        "eligibility": {"client": True, "partner": False},
        "status": "Active",
        "applicableTo": "Licensee",
        "settings": program_settings_data,
        "vendor": {"id": "ACC-001", "name": "Vendor"},
        "icon": "https://example.com/icon.png",
        "statistics": {"certificates": 1},
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "create",
        "update",
        "delete",
        "publish",
        "unpublish",
        "update_settings",
        "iterate",
    ],
)
def test_mixins_present(programs_service, method):
    result = hasattr(programs_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "create",
        "update",
        "delete",
        "publish",
        "unpublish",
        "update_settings",
        "iterate",
    ],
)
def test_async_mixins_present(async_programs_service, method):
    result = hasattr(async_programs_service, method)

    assert result is True


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("documents", DocumentService),
        ("media", MediaService),
        ("parameter_groups", ParameterGroupsService),
        ("parameters", ParametersService),
        ("templates", TemplatesService),
    ],
)
def test_property_services(programs_service, service_method, expected_service_class):
    result = getattr(programs_service, service_method)("PRG-123")

    assert isinstance(result, expected_service_class)
    assert result.endpoint_params == {"program_id": "PRG-123"}


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("documents", AsyncDocumentService),
        ("media", AsyncMediaService),
        ("parameter_groups", AsyncParameterGroupsService),
        ("parameters", AsyncParametersService),
        ("templates", AsyncTemplatesService),
    ],
)
def test_async_property_services(async_programs_service, service_method, expected_service_class):
    result = getattr(async_programs_service, service_method)("PRG-123")

    assert isinstance(result, expected_service_class)
    assert result.endpoint_params == {"program_id": "PRG-123"}


def test_update_settings(programs_service, program_settings_data):
    program_id = "PRG-123"
    expected_response = {"id": program_id, "settings": program_settings_data}
    with respx.mock:
        mock_route = respx.put(
            f"https://api.example.com/public/v1/program/programs/{program_id}/settings"
        ).mock(return_value=httpx.Response(status_code=httpx.codes.OK, json=expected_response))

        result = programs_service.update_settings(program_id, program_settings_data)

    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "PUT"
    assert request.url.path == f"/public/v1/program/programs/{program_id}/settings"
    assert result.to_dict() == expected_response


async def test_async_update_settings(async_programs_service, program_settings_data):
    program_id = "PRG-123"
    expected_response = {"id": program_id, "settings": program_settings_data}
    with respx.mock:
        mock_route = respx.put(
            f"https://api.example.com/public/v1/program/programs/{program_id}/settings"
        ).mock(return_value=httpx.Response(status_code=httpx.codes.OK, json=expected_response))

        result = await async_programs_service.update_settings(program_id, program_settings_data)

    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "PUT"
    assert request.url.path == f"/public/v1/program/programs/{program_id}/settings"
    assert result.to_dict() == expected_response


def test_sync_program_update(programs_service, tmp_path):
    program_id = "PRG-123"
    update_data = {"name": "Updated Program"}
    expected_response = {"id": program_id, "name": "Updated Program"}
    icon_path = tmp_path / "icon.png"
    icon_path.write_bytes(b"fake image data")
    with icon_path.open("rb") as icon_file, respx.mock:
        mock_route = respx.put(
            f"https://api.example.com/public/v1/program/programs/{program_id}"
        ).mock(return_value=httpx.Response(status_code=httpx.codes.OK, json=expected_response))

        result = programs_service.update(program_id, update_data, file=icon_file)

    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "PUT"
    assert request.url.path == f"/public/v1/program/programs/{program_id}"
    assert result.to_dict() == expected_response


async def test_async_program_update(async_programs_service, tmp_path):
    program_id = "PRG-123"
    update_data = {"name": "Updated Program"}
    expected_response = {"id": program_id, "name": "Updated Program"}
    icon_path = tmp_path / "icon.png"
    icon_path.write_bytes(b"fake image data")
    with icon_path.open("rb") as icon_file, respx.mock:
        mock_route = respx.put(
            f"https://api.example.com/public/v1/program/programs/{program_id}"
        ).mock(return_value=httpx.Response(status_code=httpx.codes.OK, json=expected_response))

        result = await async_programs_service.update(program_id, update_data, file=icon_file)

    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "PUT"
    assert request.url.path == f"/public/v1/program/programs/{program_id}"
    assert result.to_dict() == expected_response


def test_program_primitive_fields(program_data):
    result = Program(program_data)

    assert result.to_dict() == program_data


def test_program_nested_fields_are_base_models(program_data):
    result = Program(program_data)

    assert isinstance(result.vendor, BaseModel)
    assert isinstance(result.eligibility, BaseModel)
    assert isinstance(result.settings, BaseModel)
    assert isinstance(result.statistics, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_program_optional_fields():
    result = Program({"id": "PRG-123"})

    assert result.id == "PRG-123"
    assert not hasattr(result, "name")
    assert not hasattr(result, "website")
    assert not hasattr(result, "status")
    assert not hasattr(result, "applicable_to")
    assert not hasattr(result, "icon")
    assert not hasattr(result, "vendor")
    assert not hasattr(result, "settings")
    assert not hasattr(result, "statistics")
    assert not hasattr(result, "audit")
