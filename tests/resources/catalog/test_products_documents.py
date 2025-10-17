import pytest

from mpt_api_client.resources.catalog.products_documents import (
    AsyncDocumentService,
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


def test_endpoint(document_service) -> None:
    assert document_service.path == "/public/v1/catalog/products/PRD-001/documents"


def test_async_endpoint(async_document_service) -> None:
    assert async_document_service.path == "/public/v1/catalog/products/PRD-001/documents"


@pytest.mark.parametrize(
    "method", ["get", "create", "delete", "update", "download", "review", "publish", "unpublish"]
)
def test_methods_present(document_service, method: str) -> None:
    assert hasattr(document_service, method)


@pytest.mark.parametrize(
    "method", ["get", "create", "delete", "update", "download", "review", "publish", "unpublish"]
)
def test_async_methods_present(async_document_service, method: str) -> None:
    assert hasattr(async_document_service, method)
