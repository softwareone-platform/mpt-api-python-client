import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.program.enrollments_attachments import (
    AsyncEnrollmentAttachmentsService,
    EnrollmentAttachment,
    EnrollmentAttachmentsService,
)


@pytest.fixture
def enrollment_attachments_service(http_client):
    return EnrollmentAttachmentsService(
        http_client=http_client, endpoint_params={"enrollment_id": "ENR-123"}
    )


@pytest.fixture
def async_enrollment_attachments_service(async_http_client):
    return AsyncEnrollmentAttachmentsService(
        http_client=async_http_client, endpoint_params={"enrollment_id": "ENR-123"}
    )


@pytest.fixture
def enrollment_attachment_data():
    return {
        "name": "Attachment 1",
        "description": "This is the first attachment.",
        "type": "File",
        "filename": "attachment1.pdf",
        "size": 1024,
        "contentType": "application/pdf",
        "enrollment": {"id": "ENR-123"},
        "audit": {"created": "2024-01-01T00:00:00Z", "updated": "2024-01-02T00:00:00Z"},
    }


def test_endpoint(enrollment_attachments_service):
    result = (
        enrollment_attachments_service.path == "/public/v1/program/enrollments/ENR-123/attachments"
    )

    assert result is True


def test_async_endpoint(async_enrollment_attachments_service):
    result = (
        async_enrollment_attachments_service.path
        == "/public/v1/program/enrollments/ENR-123/attachments"
    )

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate", "download"])
def test_methods_present(enrollment_attachments_service, method: str):
    result = hasattr(enrollment_attachments_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate", "download"])
def test_async_methods_present(async_enrollment_attachments_service, method: str):
    result = hasattr(async_enrollment_attachments_service, method)

    assert result is True


def test_attachment_primitive_fields(enrollment_attachment_data):
    result = EnrollmentAttachment(enrollment_attachment_data)

    assert result.to_dict() == enrollment_attachment_data


def test_attachment_nested_fields(enrollment_attachment_data):
    result = EnrollmentAttachment(enrollment_attachment_data)

    assert isinstance(result.enrollment, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_attachment_optional_fields():
    result = EnrollmentAttachment({"id": "ENA-123"})

    assert result.id == "ENA-123"
    assert result.name is None
    assert result.description is None
    assert result.type is None
    assert result.filename is None
    assert result.size is None
    assert result.content_type is None
    assert result.enrollment is None
    assert result.audit is None
