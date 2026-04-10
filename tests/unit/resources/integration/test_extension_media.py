import httpx
import pytest
import respx

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.integration.extension_media import (
    AsyncExtensionMediaService,
    ExtensionMedia,
    ExtensionMediaService,
)
from mpt_api_client.resources.integration.extensions import (
    AsyncExtensionsService,
    ExtensionsService,
)


@pytest.fixture
def media_service(http_client) -> ExtensionMediaService:
    return ExtensionMediaService(
        http_client=http_client, endpoint_params={"extension_id": "EXT-001"}
    )


@pytest.fixture
def async_media_service(async_http_client) -> AsyncExtensionMediaService:
    return AsyncExtensionMediaService(
        http_client=async_http_client, endpoint_params={"extension_id": "EXT-001"}
    )


FILE_SIZE = 512000


@pytest.fixture
def media_data():
    return {
        "id": "MED-001",
        "name": "Extension Screenshot",
        "revision": 1,
        "type": "Image",
        "description": "Main extension screenshot",
        "status": "Draft",
        "filename": "screenshot.png",
        "size": FILE_SIZE,
        "contentType": "image/png",
        "displayOrder": 1,
        "url": "https://example.com/screenshot.png",
        "extension": {"id": "EXT-001", "name": "My Extension"},
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "create",
        "update",
        "delete",
        "download",
        "publish",
        "unpublish",
        "upload_image",
        "iterate",
    ],
)
def test_mixins_present(media_service, method: str) -> None:
    result = hasattr(media_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "create",
        "update",
        "delete",
        "download",
        "publish",
        "unpublish",
        "upload_image",
        "iterate",
    ],
)
def test_async_mixins_present(async_media_service, method: str) -> None:
    result = hasattr(async_media_service, method)

    assert result is True


def test_extension_media_primitive_fields(media_data) -> None:
    result = ExtensionMedia(media_data)

    assert result.id == "MED-001"
    assert result.name == "Extension Screenshot"
    assert result.revision == 1
    assert result.type == "Image"
    assert result.status == "Draft"
    assert result.filename == "screenshot.png"
    assert result.size == FILE_SIZE
    assert result.display_order == 1


def test_extension_media_nested_fields(media_data) -> None:  # noqa: WPS118
    result = ExtensionMedia(media_data)

    assert isinstance(result.extension, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_extension_media_create(media_service, tmp_path) -> None:
    media_payload = {"Name": "Screenshot", "MediaType": "Image", "DisplayOrder": 1}
    expected_response = {"id": "MED-001", "name": "Screenshot"}
    image_path = tmp_path / "screenshot.png"
    image_path.write_bytes(b"fake image data")
    with image_path.open("rb") as image_file, respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/integration/extensions/EXT-001/media"
        ).mock(return_value=httpx.Response(httpx.codes.CREATED, json=expected_response))

        result = media_service.create(media_payload, file=image_file)

    assert mock_route.call_count == 1
    assert mock_route.calls[0].request.method == "POST"
    assert result.to_dict() == expected_response


def test_extension_media_download(media_service) -> None:
    image_bytes = b"\x89PNG\r\n\x1a\n"
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/integration/extensions/EXT-001/media/MED-001"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "image/png"},
                content=image_bytes,
            )
        )

        result = media_service.download("MED-001", accept="image/png")

    assert mock_route.call_count == 1
    assert mock_route.calls[0].request.method == "GET"
    assert result.file_contents == image_bytes


async def test_async_extension_media_download(async_media_service) -> None:
    image_bytes = b"\x89PNG\r\n\x1a\n"
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/integration/extensions/EXT-001/media/MED-001"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "image/png"},
                content=image_bytes,
            )
        )

        result = await async_media_service.download("MED-001", accept="image/png")

    assert mock_route.call_count == 1
    assert mock_route.calls[0].request.method == "GET"
    assert result.file_contents == image_bytes


def test_extensions_media_accessor(http_client) -> None:
    extensions_service = ExtensionsService(http_client=http_client)

    result = extensions_service.media("EXT-001")

    assert isinstance(result, ExtensionMediaService)
    assert result.http_client is http_client
    assert result.path == "/public/v1/integration/extensions/EXT-001/media"


def test_async_extensions_media_accessor(async_http_client) -> None:
    extensions_service = AsyncExtensionsService(http_client=async_http_client)

    result = extensions_service.media("EXT-001")

    assert isinstance(result, AsyncExtensionMediaService)
    assert result.http_client is async_http_client
    assert result.path == "/public/v1/integration/extensions/EXT-001/media"
