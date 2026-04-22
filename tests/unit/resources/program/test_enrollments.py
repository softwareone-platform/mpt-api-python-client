import httpx
import pytest
import respx

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.program.enrollments import (
    AsyncEnrollmentService,
    Enrollment,
    EnrollmentService,
)


@pytest.fixture
def enrollment_service(http_client):
    return EnrollmentService(http_client=http_client)


@pytest.fixture
def async_enrollment_service(async_http_client):
    return AsyncEnrollmentService(http_client=async_http_client)


@pytest.fixture
def enrollment_data():
    return {
        "id": "ENR-123",
        "name": "Enrollment 123",
        "status": "active",
        "program": {"id": "PRG-123"},
        "certificate": {"id": "CRT-123"},
        "vendor": {"id": "ACC-123"},
        "applicableTo": "all",
        "type": "standard",
        "licensee": {"id": "LCE-123"},
        "eligibility": {"criteria": "must be eligible"},
        "parameters": {"param1": "value1"},
        "template": {"id": "TMP-123"},
        "audit": {"created": "2024-01-01T00:00:00Z", "updated": "2024-01-02T00:00:00Z"},
    }


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("validate", {"id": "ENR-123", "status": "updated"}),
        ("query", {"id": "ENR-123", "status": "updated"}),
        ("process", {"id": "ENR-123", "status": "updated"}),
        ("complete", {"id": "ENR-123", "status": "updated"}),
        ("submit", {"id": "ENR-123", "status": "updated"}),
        ("fail", {"id": "ENR-123", "status": "updated"}),
    ],
)
def test_custom_resource_actions(enrollment_service, action, input_status):
    request_expected_content = b'{"id":"ENR-123","status":"updated"}'
    response_expected_data = {"id": "ENR-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/program/enrollments/ENR-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(enrollment_service, action)("ENR-123", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Enrollment)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("validate", None),
        ("query", None),
        ("process", None),
        ("complete", None),
        ("submit", None),
        ("fail", None),
    ],
)
def test_custom_resource_actions_no_data(enrollment_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "ENR-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/program/enrollments/ENR-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(enrollment_service, action)("ENR-123", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Enrollment)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("validate", {"id": "ENR-123", "status": "updated"}),
        ("query", {"id": "ENR-123", "status": "updated"}),
        ("process", {"id": "ENR-123", "status": "updated"}),
        ("complete", {"id": "ENR-123", "status": "updated"}),
        ("submit", {"id": "ENR-123", "status": "updated"}),
        ("fail", {"id": "ENR-123", "status": "updated"}),
    ],
)
async def test_async_custom_resource_actions(async_enrollment_service, action, input_status):
    request_expected_content = b'{"id":"ENR-123","status":"updated"}'
    response_expected_data = {"id": "ENR-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/program/enrollments/ENR-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_enrollment_service, action)("ENR-123", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Enrollment)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("validate", None),
        ("query", None),
        ("process", None),
        ("complete", None),
        ("submit", None),
        ("fail", None),
    ],
)
async def test_async_custom_resource_actions_no_data(
    async_enrollment_service, action, input_status
):
    request_expected_content = b""
    response_expected_data = {"id": "ENR-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/program/enrollments/ENR-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_enrollment_service, action)("ENR-123", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Enrollment)


def test_enrollment_primitive_fields(enrollment_data):
    result = Enrollment(enrollment_data)

    assert result.to_dict() == enrollment_data


def test_enrollment_nested_fields(enrollment_data):
    result = Enrollment(enrollment_data)

    assert isinstance(result.program, BaseModel)
    assert isinstance(result.certificate, BaseModel)
    assert isinstance(result.vendor, BaseModel)
    assert isinstance(result.licensee, BaseModel)
    assert isinstance(result.eligibility, BaseModel)
    assert isinstance(result.parameters, BaseModel)
    assert isinstance(result.template, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_enrollment_optional_fields():
    result = Enrollment({})

    assert not hasattr(result, "name")
    assert not hasattr(result, "certificate")
    assert not hasattr(result, "program")
    assert not hasattr(result, "vendor")
    assert not hasattr(result, "applicable_to")
    assert not hasattr(result, "type")
    assert not hasattr(result, "licensee")
    assert not hasattr(result, "eligibility")
    assert not hasattr(result, "status")
    assert not hasattr(result, "parameters")
    assert not hasattr(result, "template")
    assert not hasattr(result, "audit")
