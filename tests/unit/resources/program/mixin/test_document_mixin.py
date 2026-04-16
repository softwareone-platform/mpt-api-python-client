import io

import httpx
import pytest
import respx

from mpt_api_client.http.async_service import AsyncService
from mpt_api_client.http.service import Service
from mpt_api_client.resources.program.mixins import (
    AsyncDocumentMixin,
    DocumentMixin,
)
from tests.unit.conftest import DummyModel


class DummyDocumentService(
    DocumentMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/documents"
    _model_class = DummyModel
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "document"


class DummyAsyncDocumentService(
    AsyncDocumentMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/documents"
    _model_class = DummyModel
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "document"


@pytest.fixture
def document_service(http_client):
    return DummyDocumentService(http_client=http_client)


@pytest.fixture
def async_document_service(async_http_client):
    return DummyAsyncDocumentService(http_client=async_http_client)


def test_document_create_with_url(document_service):
    resource_data = {
        "name": "Dummy Doc",
        "description": "Dummy Doc",
        "url": "https://example.com/dummyfile.pdf",
    }
    with respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/dummy/documents").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=resource_data,
            )
        )
        new_document = document_service.create(resource_data=resource_data)

    result = mock_route.calls[0].request

    assert (
        b'Content-Disposition: form-data; name="document"\r\n'
        b"Content-Type: application/json\r\n\r\n"
        b'{"name":"Dummy Doc","description":"Dummy Doc","url":"https://example.com/dummyfile.pdf"}\r\n'
        in result.content
    )
    assert b'Content-Disposition: form-data; name="file"' not in result.content
    assert "multipart/form-data" in result.headers["Content-Type"]
    assert new_document.to_dict() == resource_data
    assert isinstance(new_document, DummyModel)


def test_document_create_with_file(document_service):
    resource_data = {"id": "DOC-123", "name": "Dummy Data And File"}
    response_data = resource_data
    file_tuple = ("dummyfile.pdf", io.BytesIO(b"dummy file content"), "application/pdf")
    with respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/dummy/documents").mock(
            return_value=httpx.Response(status_code=httpx.codes.OK, json=response_data)
        )

        result = document_service.create(resource_data=resource_data, file=file_tuple)

    request = mock_route.calls[0].request
    assert (
        b'Content-Disposition: form-data; name="document"\r\n'
        b"Content-Type: application/json\r\n\r\n"
        b'{"id":"DOC-123","name":"Dummy Data And File"}\r\n' in request.content
    )
    assert (
        b'Content-Disposition: form-data; name="file"; filename="dummyfile.pdf"\r\n'
        b"Content-Type: application/pdf\r\n\r\n"
        b"dummy file content\r\n" in request.content
    )
    assert "multipart/form-data" in request.headers["Content-Type"]
    assert result.to_dict() == response_data
    assert isinstance(result, DummyModel)


async def test_async_document_create_with_url(async_document_service):
    resource_data = {
        "name": "Async Dummy Doc",
        "description": "Async Dummy Doc",
        "url": "https://example.com/async_dummyfile.pdf",
    }
    with respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/dummy/documents").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=resource_data,
            )
        )

        result = await async_document_service.create(resource_data=resource_data)

    request = mock_route.calls[0].request
    assert (
        b'Content-Disposition: form-data; name="document"\r\n'
        b"Content-Type: application/json\r\n\r\n"
        b'{"name":"Async Dummy Doc","description":"Async Dummy Doc","url":"https://example.com/async_dummyfile.pdf"}\r\n'
        in request.content
    )
    assert b'Content-Disposition: form-data; name="file"' not in request.content
    assert "multipart/form-data" in request.headers["Content-Type"]
    assert result.to_dict() == resource_data
    assert isinstance(result, DummyModel)


async def test_async_document_create_with_file(async_document_service):  # noqa: WPS210
    resource_data = {"id": "DOC-124", "name": "Async Dummy Data And File"}
    response_data = resource_data
    file_tuple = ("manual.pdf", io.BytesIO(b"PDF DATA"), "application/pdf")
    with respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/dummy/documents").mock(
            return_value=httpx.Response(status_code=httpx.codes.OK, json=response_data)
        )

        result = await async_document_service.create(resource_data=resource_data, file=file_tuple)

    request = mock_route.calls[0].request
    assert (
        b'Content-Disposition: form-data; name="document"\r\n'
        b"Content-Type: application/json\r\n\r\n"
        b'{"id":"DOC-124","name":"Async Dummy Data And File"}\r\n' in request.content
    )
    assert (
        b'Content-Disposition: form-data; name="file"; filename="manual.pdf"\r\n'
        b"Content-Type: application/pdf\r\n\r\n"
        b"PDF DATA\r\n" in request.content
    )
    assert "multipart/form-data" in request.headers["Content-Type"]
    assert result.to_dict() == response_data
    assert isinstance(result, DummyModel)
