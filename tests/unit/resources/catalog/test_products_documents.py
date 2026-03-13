import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.catalog.products_documents import (
    AsyncDocumentService,
    Document,
    DocumentService,
)


@pytest.fixture
def document_service(http_client) -> DocumentService:
    return DocumentService(http_client=http_client, endpoint_params={"product_id": "PRD-001"})


@pytest.fixture
def async_document_service(async_http_client) -> AsyncDocumentService:
    return AsyncDocumentService(
        http_client=async_http_client, endpoint_params={"product_id": "PRD-001"}
    )


@pytest.fixture
def document_data():
    return {
        "id": "DOC-001",
        "name": "User Guide",
        "type": "UserGuide",
        "description": "Product user guide",
        "status": "Active",
        "filename": "guide.pdf",
        "size": 4096,
        "contentType": "application/pdf",
        "url": "https://example.com/guide.pdf",
        "language": "en",
        "product": {"id": "PRD-001", "name": "My Product"},
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_endpoint(document_service) -> None:
    result = document_service.path == "/public/v1/catalog/products/PRD-001/documents"

    assert result is True


def test_async_endpoint(async_document_service) -> None:
    result = async_document_service.path == "/public/v1/catalog/products/PRD-001/documents"

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "delete", "update", "download", "review", "publish", "unpublish", "iterate"],
)
def test_methods_present(document_service, method: str) -> None:
    result = hasattr(document_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "delete", "update", "download", "review", "publish", "unpublish", "iterate"],
)
def test_async_methods_present(async_document_service, method: str) -> None:
    result = hasattr(async_document_service, method)

    assert result is True


def test_document_primitive_fields(document_data):
    result = Document(document_data)

    assert result.to_dict() == document_data


def test_document_nested_fields_are_base_models(document_data):
    result = Document(document_data)

    assert isinstance(result.product, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_document_optional_fields_absent():
    result = Document({"id": "DOC-001"})

    assert result.id == "DOC-001"
    assert not hasattr(result, "name")
    assert not hasattr(result, "status")
    assert not hasattr(result, "audit")
