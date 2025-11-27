import io

import httpx
import pytest
import respx

from mpt_api_client.resources.notifications.batches import (
    AsyncBatchesService,
    BatchesService,
)


@pytest.fixture
def batches_service(http_client):
    return BatchesService(http_client=http_client)


@pytest.fixture
def async_batches_service(async_http_client):
    return AsyncBatchesService(http_client=async_http_client)


@pytest.mark.parametrize("method", ["get", "create", "iterate", "get_batch_attachment"])
def test_sync_batches_service_methods(batches_service, method):
    result = hasattr(batches_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "iterate", "get_batch_attachment"])
def test_async_batches_service_methods(async_batches_service, method):
    result = hasattr(async_batches_service, method)

    assert result is True


def test_sync_get_batch_attachment(batches_service):
    attachment_content = b"Attachment file content or binary data"
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/notifications/batches/BAT-123/attachments/ATT-456"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={
                    "content-type": "application/octet-stream",
                    "content-disposition": (
                        'form-data; name="file"; filename="batch_attachment.pdf"'
                    ),
                },
                content=attachment_content,
            )
        )

        result = batches_service.get_batch_attachment("BAT-123", "ATT-456")

        assert mock_route.call_count == 1
        assert result.file_contents == attachment_content
        assert result.content_type == "application/octet-stream"
        assert result.filename == "batch_attachment.pdf"


@pytest.mark.asyncio
async def test_async_get_batch_attachment(async_batches_service):
    attachment_content = b"Attachment file content or binary data"
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/notifications/batches/BAT-123/attachments/ATT-456"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={
                    "content-type": "application/octet-stream",
                    "content-disposition": (
                        'form-data; name="file"; filename="batch_attachment.pdf"'
                    ),
                },
                content=attachment_content,
            )
        )

        result = await async_batches_service.get_batch_attachment("BAT-123", "ATT-456")

        assert mock_route.call_count == 1
        assert result.file_contents == attachment_content
        assert result.content_type == "application/octet-stream"
        assert result.filename == "batch_attachment.pdf"


def test_sync_batches_create_with_data(batches_service):
    batch_data = {"name": "Test Batch"}
    with respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/notifications/batches").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json={"id": "BAT-133", "name": "Test Batch"},
            )
        )
        files = {"attachment": ("test.pdf", io.BytesIO(b"PDF content"), "application/pdf")}

        result = batches_service.create(batch_data, files=files)

        request = mock_route.calls[0].request
        assert b'Content-Disposition: form-data; name="_attachment_data"' in request.content
        assert mock_route.call_count == 1
        assert result.id == "BAT-133"
        assert result.name == "Test Batch"


@pytest.mark.asyncio
async def test_async_batches_create_with_data(async_batches_service):
    batch_data = {"name": "Test Batch"}
    with respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/notifications/batches").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json={"id": "BAT-133", "name": "Test Batch"},
            )
        )
        files = {"attachment": ("test.pdf", io.BytesIO(b"PDF content"), "application/pdf")}

        result = await async_batches_service.create(batch_data, files=files)

        request = mock_route.calls[0].request
        assert b'Content-Disposition: form-data; name="_attachment_data"' in request.content
        assert mock_route.call_count == 1
        assert result.id == "BAT-133"
        assert result.name == "Test Batch"
