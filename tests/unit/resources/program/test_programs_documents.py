import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.program.programs_documents import (
    AsyncDocumentService,
    Document,
    DocumentService,
)


@pytest.fixture
def document_service(http_client) -> DocumentService:
    return DocumentService(http_client=http_client, endpoint_params={"program_id": "PRG-123"})


@pytest.fixture
def async_document_service(async_http_client) -> AsyncDocumentService:
    return AsyncDocumentService(
        http_client=async_http_client, endpoint_params={"program_id": "PRG-123"}
    )


@pytest.fixture
def document_data():
    return {
        "id": "PDM-001",
        "name": "Program Overview",
        "type": "Overview",
        "description": "Overview of the program",
        "status": "Active",
        "filename": "overview.pdf",
        "size": 2048,
        "contentType": "application/pdf",
        "url": "https://example.com/overview.pdf",
        "language": "en",
        "program": {"id": "PRG-123", "name": "My Program"},
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_endpoint(document_service):
    result = document_service.path == "/public/v1/program/programs/PRG-123/documents"

    assert result is True


def test_async_endpoint(async_document_service):
    result = async_document_service.path == "/public/v1/program/programs/PRG-123/documents"

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "delete", "update", "download", "publish", "unpublish", "iterate"],
)
def test_methods_present(document_service, method):
    result = hasattr(document_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "delete", "update", "download", "publish", "unpublish", "iterate"],
)
def test_async_methods_present(async_document_service, method):
    result = hasattr(async_document_service, method)

    assert result is True


def test_document_primitive_fields(document_data):
    result = Document(document_data)

    assert result.to_dict() == document_data


def test_document_inherited_primitive_fields(document_inherited_data):
    result = Document(document_inherited_data)

    assert result.to_dict() == document_inherited_data


def test_document_nested_fields_are_base_models(document_data):
    result = Document(document_data)

    assert isinstance(result.program, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_document_optional_fields_absent():
    result = Document({"id": "PDM-001"})

    assert result.id == "PDM-001"
    assert result.name is None
    assert result.type is None
    assert result.description is None
    assert result.status is None
    assert result.filename is None
    assert result.size is None
    assert result.content_type is None
    assert result.url is None
    assert result.program is None
    assert result.audit is None
