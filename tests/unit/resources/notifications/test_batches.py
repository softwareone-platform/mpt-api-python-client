import pytest

from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.http.types import Response
from mpt_api_client.models import FileModel
from mpt_api_client.resources.notifications.batches import (
    AsyncBatchesService,
    BatchAttachment,
    BatchesService,
)


@pytest.fixture
def batches_service(http_client: HTTPClient) -> BatchesService:
    return BatchesService(http_client=http_client)


@pytest.fixture
def async_batches_service(async_http_client: AsyncHTTPClient) -> AsyncBatchesService:
    return AsyncBatchesService(http_client=async_http_client)


@pytest.fixture
def attachment_response() -> Response:
    return Response(
        headers={"content-disposition": 'attachment; filename="test.csv"'},
        status_code=200,
        content=b"content",
    )


@pytest.fixture
def batch_attachment_response() -> Response:
    return Response(
        headers={"Content-Type": "application/json"},
        status_code=200,
        content=b'{"id": "A-123", "name": "test.csv"}',
    )


@pytest.mark.parametrize(
    "method", ["get", "create", "iterate", "download_attachment", "get_attachment"]
)
def test_sync_batches_service_methods(batches_service: BatchesService, method: str) -> None:
    result = hasattr(batches_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method", ["get", "create", "iterate", "download_attachment", "get_attachment"]
)
def test_async_batches_service_methods(
    async_batches_service: AsyncBatchesService, method: str
) -> None:
    result = hasattr(async_batches_service, method)

    assert result is True


def test_get_attachment(mocker, batches_service, batch_attachment_response) -> None:
    batch_id = "B-123"
    attachment_id = "A-123"
    mock_request = mocker.patch.object(
        batches_service.http_client, "request", return_value=batch_attachment_response
    )

    result = batches_service.get_attachment(batch_id, attachment_id)

    assert isinstance(result, BatchAttachment)
    assert result.id == "A-123"
    mock_request.assert_called_once_with(
        "get",
        f"/public/v1/notifications/batches/{batch_id}/attachments/{attachment_id}",
        headers={"Accept": "application/json"},
    )


async def test_async_get_attachment(
    mocker, async_batches_service, batch_attachment_response
) -> None:
    batch_id = "B-123"
    attachment_id = "A-123"
    mock_request = mocker.patch.object(
        async_batches_service.http_client, "request", return_value=batch_attachment_response
    )

    result = await async_batches_service.get_attachment(batch_id, attachment_id)

    assert isinstance(result, BatchAttachment)
    assert result.id == "A-123"
    mock_request.assert_called_once_with(
        "get",
        f"/public/v1/notifications/batches/{batch_id}/attachments/{attachment_id}",
        headers={"Accept": "application/json"},
    )


def test_download_attachment(mocker, batches_service, attachment_response) -> None:
    batch_id = "B-123"
    attachment_id = "A-123"
    mock_request = mocker.patch.object(
        batches_service.http_client, "request", return_value=attachment_response
    )

    result = batches_service.download_attachment(batch_id, attachment_id)

    assert isinstance(result, FileModel)
    mock_request.assert_called_once_with(
        "get", f"/public/v1/notifications/batches/{batch_id}/attachments/{attachment_id}"
    )


async def test_async_download_attachment(  # noqa: WPS210
    mocker, async_batches_service, attachment_response
) -> None:
    batch_id = "B-123"
    attachment_id = "A-123"
    mock_request = mocker.patch.object(
        async_batches_service.http_client, "request", return_value=attachment_response
    )

    result = await async_batches_service.download_attachment(batch_id, attachment_id)

    assert isinstance(result, FileModel)

    mock_request.assert_called_once_with(
        "get", f"/public/v1/notifications/batches/{batch_id}/attachments/{attachment_id}"
    )
