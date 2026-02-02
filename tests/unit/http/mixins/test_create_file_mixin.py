import io

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


async def test_async_file_create_with_data(async_media_service: AsyncMediaService) -> None:
    """Test creating a file resource asynchronously with additional data."""
    media_data = {"id": "MED-133"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=media_data,
            )
        )
        media_image = ("test.jpg", io.BytesIO(b"Image content"), "image/jpeg")

        result = await async_media_service.create({"name": "Product image"}, file=media_image)

    request = mock_route.calls[0].request
    assert (
        b'Content-Disposition: form-data; name="media"\r\n'
        b"Content-Type: application/json\r\n\r\n"
        b'{"name":"Product image"}\r\n' in request.content
    )
    assert (
        b'Content-Disposition: form-data; name="file"; filename="test.jpg"\r\n'
        b"Content-Type: image/jpeg\r\n\r\n"
        b"Image content\r\n" in request.content
    )
    assert "multipart/form-data" in request.headers["Content-Type"]
    assert result.to_dict() == media_data


async def test_async_file_create_no_data(async_media_service: AsyncMediaService) -> None:
    """Test creating a file resource asynchronously without additional data."""
    media_data = {"id": "MED-133"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=media_data,
            )
        )
        new_media = await async_media_service.create(
            {}, file=("test.jpg", io.BytesIO(b"Image content"), "image/jpeg")
        )

    request = mock_route.calls[0].request

    assert (
        b'Content-Disposition: form-data; name="file"; filename="test.jpg"\r\n'
        b"Content-Type: image/jpeg\r\n\r\n"
        b"Image content\r\n" in request.content
    )
    assert new_media.to_dict() == media_data


def test_sync_file_create_with_data(media_service: MediaService) -> None:
    """Test creating a file resource synchronously with additional data."""
    media_data = {"id": "MED-133"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=media_data,
            )
        )
        image_file = ("test.jpg", io.BytesIO(b"Image content"), "image/jpeg")

        result = media_service.create({"name": "Product image"}, image_file)

    request = mock_route.calls[0].request
    assert (
        b'Content-Disposition: form-data; name="media"\r\n'
        b"Content-Type: application/json\r\n\r\n"
        b'{"name":"Product image"}\r\n' in request.content
    )
    assert (
        b'Content-Disposition: form-data; name="file"; filename="test.jpg"\r\n'
        b"Content-Type: image/jpeg\r\n\r\n"
        b"Image content\r\n" in request.content
    )
    assert "multipart/form-data" in request.headers["Content-Type"]
    assert result.to_dict() == media_data


def test_sync_file_create_no_data(media_service: MediaService) -> None:
    """Test creating a file resource synchronously without additional data."""
    media_data = {"id": "MED-133"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=media_data,
            )
        )
        image_file = ("test.jpg", io.BytesIO(b"Image content"), "image/jpeg")

        result = media_service.create({}, image_file)

    request = mock_route.calls[0].request
    assert (
        b'Content-Disposition: form-data; name="file"; filename="test.jpg"\r\n'
        b"Content-Type: image/jpeg\r\n\r\n"
        b"Image content\r\n" in request.content
    )
    assert result.to_dict() == media_data
