from http import HTTPStatus

import httpx
import pytest
import respx

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.program.certificates import (
    AsyncCertificateService,
    Certificate,
    CertificateService,
)


@pytest.fixture
def certificate_service(http_client):
    return CertificateService(http_client=http_client)


@pytest.fixture
def async_certificate_service(async_http_client):
    return AsyncCertificateService(http_client=async_http_client)


@pytest.fixture
def certificate_data():
    return {
        "id": "CER-123",
        "name": "Certificate 123",
        "program": {"id": "PRG-123"},
        "vendor": {"id": "ACC-123"},
        "externalIds": {"extId1": "value1"},
        "client": {"id": "ACC-123"},
        "applicableTo": "all",
        "licensee": {"id": "LCE-123"},
        "eligibility": {"criteria": "must be eligible"},
        "status": "active",
        "statusNotes": "Certificate is active",
        "parameters": {"param1": "value1"},
        "audit": {"created": "2024-01-01T00:00:00Z", "updated": "2024-01-02T00:00:00Z"},
    }


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("terminate", {"id": "CER-123", "status": "updated"}),
    ],
)
def test_custom_resource_actions(certificate_service, action, input_status):
    request_expected_content = b'{"id":"CER-123","status":"updated"}'
    response_expected_data = {"id": "CER-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/program/certificates/CER-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=HTTPStatus.OK,
                headers={"Content-Type": "application/json"},
                json=response_expected_data,
            )
        )

        result = certificate_service.terminate("CER-123", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Certificate)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("terminate", {"id": "CER-123", "status": "updated"}),
    ],
)
async def test_async_custom_resource_actions(async_certificate_service, action, input_status):
    request_expected_content = b'{"id":"CER-123","status":"updated"}'
    response_expected_data = {"id": "CER-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/program/certificates/CER-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=HTTPStatus.OK,
                headers={"Content-Type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await async_certificate_service.terminate("CER-123", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Certificate)


def test_certificate_primitive_fields(certificate_data):
    result = Certificate(certificate_data)

    assert result.to_dict() == certificate_data


def test_certificate_nested_fields(certificate_data):
    result = Certificate(certificate_data)

    assert isinstance(result.program, BaseModel)
    assert isinstance(result.vendor, BaseModel)
    assert isinstance(result.client, BaseModel)
    assert isinstance(result.licensee, BaseModel)
    assert isinstance(result.eligibility, BaseModel)
    assert isinstance(result.parameters, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_certificate_optional_fields():
    result = Certificate({"id": "CER-123"})

    assert result.id == "CER-123"
    assert not hasattr(result, "name")
    assert not hasattr(result, "program")
    assert not hasattr(result, "vendor")
    assert not hasattr(result, "external_ids")
    assert not hasattr(result, "client")
    assert not hasattr(result, "applicable_to")
    assert not hasattr(result, "licensee")
    assert not hasattr(result, "eligibility")
    assert not hasattr(result, "status")
    assert not hasattr(result, "status_notes")
    assert not hasattr(result, "parameters")
    assert not hasattr(result, "audit")
