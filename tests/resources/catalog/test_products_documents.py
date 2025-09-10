import io

import httpx
import pytest
import respx

from mpt_api_client.resources.catalog.products_documents import (
    AsyncDocumentService,
    DocumentService,
)


@pytest.fixture
def document_service(http_client):
    return DocumentService(http_client=http_client, endpoint_params={"product_id": "PRD-001"})


@pytest.fixture
def async_document_service(async_http_client):
    return AsyncDocumentService(
        http_client=async_http_client, endpoint_params={"product_id": "PRD-001"}
    )


def test_endpoint(document_service):
    assert document_service.endpoint == "/public/v1/catalog/products/PRD-001/documents"


def test_async_endpoint(async_document_service):
    assert async_document_service.endpoint == "/public/v1/catalog/products/PRD-001/documents"


async def test_async_create(async_document_service):
    document_data = {"id": "DOC-133"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/catalog/products/PRD-001/documents"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                json=document_data,
            )
        )
        files = {"document": ("test.pdf", io.BytesIO(b"PDF content"), "application/pdf")}
        new_document = await async_document_service.create(
            {"name": "Product document"}, files=files
        )

    request = mock_route.calls[0].request

    assert (
        b'Content-Disposition: form-data; name="_attachment_data"\r\n'
        b"Content-Type: application/json\r\n\r\n"
        b'{"name":"Product document"}\r\n' in request.content
    )
    assert (
        b'Content-Disposition: form-data; name="document"; filename="test.pdf"\r\n'
        b"Content-Type: application/pdf\r\n\r\n"
        b"PDF content\r\n" in request.content
    )
    assert new_document.to_dict() == document_data


async def test_async_create_no_data(async_document_service):
    document_data = {"id": "DOC-133"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/catalog/products/PRD-001/documents"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                json=document_data,
            )
        )
        files = {"document": ("test.pdf", io.BytesIO(b"PDF content"), "application/pdf")}
        new_document = await async_document_service.create(files=files)

    request = mock_route.calls[0].request

    assert (
        b'Content-Disposition: form-data; name="document"; filename="test.pdf"\r\n'
        b"Content-Type: application/pdf\r\n\r\n"
        b"PDF content\r\n" in request.content
    )
    assert new_document.to_dict() == document_data


async def test_async_download(async_document_service):
    document_content = b"PDF file content or binary data"

    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/documents/DOC-456"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={
                    "content-type": "application/octet-stream",
                    "content-disposition": 'form-data; name="file"; '
                    'filename="product_document.pdf"',
                },
                content=document_content,
            )
        )

        file_model = await async_document_service.download("DOC-456")

    assert mock_route.called
    assert file_model.response.status_code == 200
    assert file_model.response.content == document_content
    assert file_model.filename == "product_document.pdf"


def test_create(document_service):
    document_data = {"id": "DOC-133"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/catalog/products/PRD-001/documents"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                json=document_data,
            )
        )
        files = {"document": ("test.pdf", io.BytesIO(b"PDF content"), "application/pdf")}
        new_document = document_service.create({"name": "Product document"}, files=files)

    request = mock_route.calls[0].request

    assert (
        b'Content-Disposition: form-data; name="_attachment_data"\r\n'
        b"Content-Type: application/json\r\n\r\n"
        b'{"name":"Product document"}\r\n' in request.content
    )
    assert (
        b'Content-Disposition: form-data; name="document"; filename="test.pdf"\r\n'
        b"Content-Type: application/pdf\r\n\r\n"
        b"PDF content\r\n" in request.content
    )
    assert new_document.to_dict() == document_data


def test_create_no_data(document_service):
    document_data = {"id": "DOC-133"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/catalog/products/PRD-001/documents"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                json=document_data,
            )
        )
        files = {"document": ("test.pdf", io.BytesIO(b"PDF content"), "application/pdf")}
        new_document = document_service.create(files=files)

    request = mock_route.calls[0].request

    assert (
        b'Content-Disposition: form-data; name="document"; filename="test.pdf"\r\n'
        b"Content-Type: application/pdf\r\n\r\n"
        b"PDF content\r\n" in request.content
    )
    assert new_document.to_dict() == document_data


def test_download(document_service):
    document_content = b"PDF file content or binary data"

    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/documents/DOC-456"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={
                    "content-type": "application/octet-stream",
                    "content-disposition": 'form-data; name="file"; '
                    'filename="product_document.pdf"',
                },
                content=document_content,
            )
        )

        file_model = document_service.download("DOC-456")

    assert mock_route.called
    assert file_model.response.status_code == 200
    assert file_model.response.content == document_content
    assert file_model.filename == "product_document.pdf"
