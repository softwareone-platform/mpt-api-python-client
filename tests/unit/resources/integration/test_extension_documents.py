import httpx
import pytest
import respx

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.integration.extension_documents import (
    AsyncExtensionDocumentsService,
    ExtensionDocument,
    ExtensionDocumentsService,
)
from mpt_api_client.resources.integration.extensions import (
    AsyncExtensionsService,
    ExtensionsService,
)


@pytest.fixture
def extension_documents_service(http_client) -> ExtensionDocumentsService:
    return ExtensionDocumentsService(
        http_client=http_client, endpoint_params={"extension_id": "EXT-001"}
    )


@pytest.fixture
def async_extension_documents_service(async_http_client) -> AsyncExtensionDocumentsService:
    return AsyncExtensionDocumentsService(
        http_client=async_http_client, endpoint_params={"extension_id": "EXT-001"}
    )


@pytest.fixture
def extensions_service(http_client) -> ExtensionsService:
    return ExtensionsService(http_client=http_client)


@pytest.fixture
def async_extensions_service(async_http_client) -> AsyncExtensionsService:
    return AsyncExtensionsService(http_client=async_http_client)


@pytest.fixture
def document_data():
    return {
        "id": "DOC-001",
        "name": "User Guide",
        "revision": 1,
        "type": "File",
        "description": "Extension user guide",
        "status": "Draft",
        "filename": "guide.pdf",
        "size": 4096,
        "contentType": "application/pdf",
        "url": "https://example.com/guide.pdf",
        "language": "en",
        "extension": {"id": "EXT-001", "name": "My Extension"},
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_endpoint(extension_documents_service) -> None:
    result = (
        extension_documents_service.path == "/public/v1/integration/extensions/EXT-001/documents"
    )

    assert result is True


def test_async_endpoint(async_extension_documents_service) -> None:
    result = (
        async_extension_documents_service.path
        == "/public/v1/integration/extensions/EXT-001/documents"
    )

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "publish", "unpublish", "iterate"],
)
def test_mixins_present(extension_documents_service, method: str) -> None:
    result = hasattr(extension_documents_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "publish", "unpublish", "iterate"],
)
def test_async_mixins_present(async_extension_documents_service, method: str) -> None:
    result = hasattr(async_extension_documents_service, method)

    assert result is True


def test_extension_document_primitive_fields(document_data):
    result = ExtensionDocument(document_data)

    assert result.to_dict() == document_data


def test_extension_document_nested_fields(document_data):
    result = ExtensionDocument(document_data)

    assert isinstance(result.extension, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_extension_document_optional_absent():
    result = ExtensionDocument({"id": "DOC-001"})

    assert result.id == "DOC-001"
    assert not hasattr(result, "name")
    assert not hasattr(result, "status")
    assert not hasattr(result, "audit")


def test_extension_document_create(extension_documents_service, tmp_path):
    document_data = {"Name": "User Guide", "Description": "Guide", "Language": "en"}
    expected_response = {"id": "DOC-001", "name": "User Guide"}
    file_path = tmp_path / "guide.pdf"
    file_path.write_bytes(b"fake pdf data")
    with file_path.open("rb") as doc_file, respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/integration/extensions/EXT-001/documents"
        ).mock(return_value=httpx.Response(httpx.codes.CREATED, json=expected_response))

        result = extension_documents_service.create(document_data, file=doc_file)

    assert mock_route.call_count == 1
    assert mock_route.calls[0].request.method == "POST"
    assert result.to_dict() == expected_response


def test_extensions_documents_accessor(extensions_service):
    result = extensions_service.documents("EXT-001")

    assert isinstance(result, ExtensionDocumentsService)
    assert result.path == "/public/v1/integration/extensions/EXT-001/documents"


def test_async_extensions_documents_accessor(async_extensions_service):
    result = async_extensions_service.documents("EXT-001")

    assert isinstance(result, AsyncExtensionDocumentsService)
    assert result.path == "/public/v1/integration/extensions/EXT-001/documents"
