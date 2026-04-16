import httpx
import pytest
import respx

from mpt_api_client.http.async_service import AsyncService
from mpt_api_client.http.service import Service
from mpt_api_client.resources.program.mixins.media_mixin import (
    AsyncMediaMixin,
    MediaMixin,
)
from tests.unit.conftest import DummyModel


class DummyMediaService(
    MediaMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/media"
    _model_class = DummyModel
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "media"


class DummyAsyncMediaService(
    AsyncMediaMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/media"
    _model_class = DummyModel
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "media"


@pytest.fixture
def media_service(http_client):
    return DummyMediaService(http_client=http_client)


@pytest.fixture
def async_media_service(async_http_client):
    return DummyAsyncMediaService(http_client=async_http_client)


@pytest.mark.parametrize("method", ["create", "download", "publish", "unpublish"])
def test_mixins_present(media_service, method):
    result = hasattr(media_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["create", "download", "publish", "unpublish"])
def test_async_mixins_present(async_media_service, method):
    result = hasattr(async_media_service, method)

    assert result is True


def test_media_download(media_service):
    image_bytes = b"\x89PNG\r\n\x1a\n"
    with respx.mock:
        mock_route = respx.get("https://api.example.com/public/v1/dummy/media/MED-123").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "image/png"},
                content=image_bytes,
            )
        )

        result = media_service.download("MED-123", accept="image/png")

    assert mock_route.call_count == 1
    assert mock_route.calls[0].request.method == "GET"
    assert result.file_contents == image_bytes


async def test_async_media_download(async_media_service):
    image_bytes = b"\x89PNG\r\n\x1a\n"
    with respx.mock:
        mock_route = respx.get("https://api.example.com/public/v1/dummy/media/MED-123").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "image/png"},
                content=image_bytes,
            )
        )

        result = await async_media_service.download("MED-123", accept="image/png")

    assert mock_route.call_count == 1
    assert mock_route.calls[0].request.method == "GET"
    assert result.file_contents == image_bytes
