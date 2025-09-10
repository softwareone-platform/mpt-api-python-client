import io

import httpx
import pytest
import respx

from mpt_api_client.resources.catalog.products_media import (
    AsyncMediaService,
    MediaService,
)


@pytest.fixture
def media_service(http_client):
    return MediaService(http_client=http_client, endpoint_params={"product_id": "PRD-001"})


@pytest.fixture
def async_media_service(async_http_client):
    return AsyncMediaService(
        http_client=async_http_client, endpoint_params={"product_id": "PRD-001"}
    )


def test_endpoint(media_service):
    assert media_service.endpoint == "/public/v1/catalog/products/PRD-001/media"


def test_async_endpoint(async_media_service):
    assert async_media_service.endpoint == "/public/v1/catalog/products/PRD-001/media"


async def test_async_create(async_media_service):
    media_data = {"id": "MED-133"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                json=media_data,
            )
        )
        files = {"media": ("test.jpg", io.BytesIO(b"Image content"), "image/jpeg")}
        new_media = await async_media_service.create({"name": "Product image"}, files=files)

    request: httpx.Request = mock_route.calls[0].request

    assert (
        b'Content-Disposition: form-data; name="_media_data"\r\n'
        b"Content-Type: application/json\r\n\r\n"
        b'{"name":"Product image"}\r\n' in request.content
    )
    assert (
        b'Content-Disposition: form-data; name="media"; filename="test.jpg"\r\n'
        b"Content-Type: image/jpeg\r\n\r\n"
        b"Image content\r\n" in request.content
    )
    assert new_media.to_dict() == media_data


async def test_async_create_no_data(async_media_service):
    media_data = {"id": "MED-133"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                json=media_data,
            )
        )
        files = {"media": ("test.jpg", io.BytesIO(b"Image content"), "image/jpeg")}
        new_media = await async_media_service.create(files=files)

    request: httpx.Request = mock_route.calls[0].request

    assert (
        b'Content-Disposition: form-data; name="media"; filename="test.jpg"\r\n'
        b"Content-Type: image/jpeg\r\n\r\n"
        b"Image content\r\n" in request.content
    )
    assert new_media.to_dict() == media_data


async def test_async_download(async_media_service):
    media_content = b"Image file content or binary data"

    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media/MED-456"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={
                    "content-type": "application/octet-stream",
                    "content-disposition": 'form-data; name="file"; filename="product_image.jpg"',
                },
                content=media_content,
            )
        )

        downloaded_file = await async_media_service.download("MED-456")
        request = mock_route.calls[0].request
        accept_header = (b"Accept", b"*")
        assert accept_header in request.headers.raw
        assert mock_route.call_count == 1
        assert downloaded_file.file_contents == media_content
        assert downloaded_file.content_type == "application/octet-stream"
        assert downloaded_file.filename == "product_image.jpg"


def test_download(media_service):
    media_content = b"Image file content or binary data"

    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media/MED-456"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={
                    "content-type": "application/octet-stream",
                    "content-disposition": 'form-data; name="file"; filename="product_image.jpg"',
                },
                content=media_content,
            )
        )

        downloaded_file = media_service.download("MED-456")
        request = mock_route.calls[0].request
        accept_header = (b"Accept", b"*")
        assert accept_header in request.headers.raw
        assert mock_route.call_count == 1
        assert downloaded_file.file_contents == media_content
        assert downloaded_file.content_type == "application/octet-stream"
        assert downloaded_file.filename == "product_image.jpg"


def test_create(media_service):
    media_data = {"id": "MED-133"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                json=media_data,
            )
        )
        files = {"media": ("test.jpg", io.BytesIO(b"Image content"), "image/jpeg")}
        new_media = media_service.create({"name": "Product image"}, files=files)

    request: httpx.Request = mock_route.calls[0].request

    assert (
        b'Content-Disposition: form-data; name="_media_data"\r\n'
        b"Content-Type: application/json\r\n\r\n"
        b'{"name":"Product image"}\r\n' in request.content
    )
    assert (
        b'Content-Disposition: form-data; name="media"; filename="test.jpg"\r\n'
        b"Content-Type: image/jpeg\r\n\r\n"
        b"Image content\r\n" in request.content
    )
    assert new_media.to_dict() == media_data


def test_create_no_data(media_service):
    media_data = {"id": "MED-133"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                json=media_data,
            )
        )
        files = {"media": ("test.jpg", io.BytesIO(b"Image content"), "image/jpeg")}
        new_media = media_service.create(files=files)

    request: httpx.Request = mock_route.calls[0].request

    assert (
        b'Content-Disposition: form-data; name="media"; filename="test.jpg"\r\n'
        b"Content-Type: image/jpeg\r\n\r\n"
        b"Image content\r\n" in request.content
    )
    assert new_media.to_dict() == media_data


@pytest.mark.parametrize(
    "method", ["get", "create", "delete", "update", "download", "review", "publish", "unpublish"]
)
def test_methods_present(media_service, method):
    assert hasattr(media_service, method)


@pytest.mark.parametrize(
    "method", ["get", "create", "delete", "update", "download", "review", "publish", "unpublish"]
)
def test_async_methods_present(async_media_service, method):
    assert hasattr(async_media_service, method)
