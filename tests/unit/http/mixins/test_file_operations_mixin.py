import io

import httpx
import pytest
import respx

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import AsyncFilesOperationsMixin, FilesOperationsMixin
from tests.unit.conftest import DummyModel


class DummyFileOperationsService(
    FilesOperationsMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/file-ops/"
    _model_class = DummyModel
    _collection_key = "data"


class DummyAsyncFileOperationsService(
    AsyncFilesOperationsMixin[DummyModel],
    AsyncService[DummyModel],
):
    """Dummy asynchronous file operations service for testing."""

    _endpoint = "/public/v1/dummy/file-ops/"
    _model_class = DummyModel
    _collection_key = "data"


@pytest.fixture
def dummy_file_operations_service(http_client) -> DummyFileOperationsService:
    """Fixture for DummyFileOperationsService."""
    return DummyFileOperationsService(http_client=http_client)


@pytest.fixture
def async_dummy_file_operations_service(async_http_client) -> DummyAsyncFileOperationsService:
    """Fixture for DummyAsyncFileOperationsService."""
    return DummyAsyncFileOperationsService(http_client=async_http_client)


def test_sync_file_create_with_resource_data(
    dummy_file_operations_service: DummyFileOperationsService,
) -> None:
    """Test creating a file with resource data."""
    file_data = {"id": "FILE-123"}
    with respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/dummy/file-ops/").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=file_data,
            )
        )
        files = {"file": ("document.pdf", io.BytesIO(b"PDF content"), "application/pdf")}
        resource_data = {"name": "Test Document"}

        result = dummy_file_operations_service.create(resource_data=resource_data, files=files)

        request = mock_route.calls[0].request
    assert b'name="_attachment_data"' in request.content
    assert b'"name":"Test Document"' in request.content
    assert result.to_dict() == file_data


async def test_async_file_create_with_resource_data(
    async_dummy_file_operations_service: DummyAsyncFileOperationsService,
) -> None:
    """Test creating a file with resource data."""
    file_data = {"id": "FILE-123"}
    with respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/dummy/file-ops/").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=file_data,
            )
        )
        files = {"file": ("document.pdf", io.BytesIO(b"PDF content"), "application/pdf")}
        resource_data = {"name": "Test Document"}
        result = await async_dummy_file_operations_service.create(
            resource_data=resource_data, files=files
        )
        request = mock_route.calls[0].request
    assert b'name="_attachment_data"' in request.content
    assert b'"name":"Test Document"' in request.content
    assert result.to_dict() == file_data
