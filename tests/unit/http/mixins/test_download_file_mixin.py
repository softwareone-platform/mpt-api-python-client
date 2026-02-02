import httpx
import pytest
import respx

from mpt_api_client.resources.catalog.products_media import AsyncMediaService, MediaService


@pytest.fixture
def media_service(http_client) -> MediaService:
    """Fixture for MediaService."""
    return MediaService(http_client=http_client, endpoint_params={"product_id": "PRD-001"})


@pytest.fixture
def async_media_service(async_http_client) -> AsyncMediaService:
    """Fixture for AsyncMediaService."""
    return AsyncMediaService(
        http_client=async_http_client, endpoint_params={"product_id": "PRD-001"}
    )


async def test_async_file_download_request_and_headers(
    async_media_service: AsyncMediaService,
) -> None:
    """Test request/response and headers for async file download."""
    media_content = b"Image file content or binary data"
    with respx.mock:
        mock_resource = respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media/MED-456",
            headers={"Accept": "application/json"},
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json={"id": "MED-456", "name": "Product image", "content_type": "image/jpg"},
            )
        )
        mock_download = respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media/MED-456",
            headers={"Accept": "image/jpg"},
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={
                    "content-type": "image/jpg",
                    "content-disposition": 'form-data; name="file"; filename="product_image.jpg"',
                },
                content=media_content,
            )
        )
        # Act
        await async_media_service.download("MED-456")

    assert mock_resource.call_count == 1
    request = mock_download.calls[0].request
    accept_header = (b"Accept", b"image/jpg")
    assert accept_header in request.headers.raw
    assert mock_download.call_count == 1


async def test_async_file_download_content_and_metadata(
    async_media_service: AsyncMediaService,
) -> None:
    """Test file content and metadata for async file download."""
    media_content = b"Image file content or binary data"
    with respx.mock:
        respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media/MED-456",
            headers={"Accept": "application/json"},
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json={"id": "MED-456", "name": "Product image", "content_type": "image/jpg"},
            )
        )
        respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media/MED-456",
            headers={"Accept": "image/jpg"},
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={
                    "content-type": "image/jpg",
                    "content-disposition": 'form-data; name="file"; filename="product_image.jpg"',
                },
                content=media_content,
            )
        )
        result = await async_media_service.download("MED-456")

    assert result.file_contents == media_content
    assert result.content_type == "image/jpg"
    assert result.filename == "product_image.jpg"


def test_sync_file_download_request_and_headers(media_service: MediaService) -> None:
    """Test request/response and headers for sync file download."""
    media_content = b"Image file content or binary data"
    with respx.mock:
        mock_resource = respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media/MED-456",
            headers={"Accept": "application/json"},
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json={"id": "MED-456", "name": "Product image", "content_type": "image/jpg"},
            )
        )
        mock_download = respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media/MED-456",
            headers={"Accept": "image/jpg"},
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={
                    "content-type": "image/jpg",
                    "content-disposition": 'form-data; name="file"; filename="product_image.jpg"',
                },
                content=media_content,
            )
        )
        media_service.download("MED-456")
    assert mock_resource.call_count == 1

    result = mock_download.calls[0].request

    # Assert
    accept_header = (b"Accept", b"image/jpg")
    assert accept_header in result.headers.raw
    assert mock_download.call_count == 1


def test_sync_file_download_content_and_metadata(media_service: MediaService) -> None:
    """Test file content and metadata for sync file download."""
    media_content = b"Image file content or binary data"
    with respx.mock:
        respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media/MED-456",
            headers={"Accept": "application/json"},
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json={"id": "MED-456", "name": "Product image", "content_type": "image/jpg"},
            )
        )
        respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media/MED-456",
            headers={"Accept": "image/jpg"},
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={
                    "content-type": "image/jpg",
                    "content-disposition": 'form-data; name="file"; filename="product_image.jpg"',
                },
                content=media_content,
            )
        )

        result = media_service.download("MED-456")

    assert result.file_contents == media_content
    assert result.content_type == "image/jpg"
    assert result.filename == "product_image.jpg"
