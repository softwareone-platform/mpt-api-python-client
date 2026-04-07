import httpx
import pytest
import respx

from mpt_api_client.http.async_service import AsyncService
from mpt_api_client.http.service import Service
from mpt_api_client.resources.integration.mixins import (
    AsyncMediaMixin,
    MediaMixin,
)
from tests.unit.conftest import DummyModel


class DummyMediaService(
    MediaMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/integration/extensions/EXT-001/media"
    _model_class = DummyModel
    _collection_key = "data"


class DummyAsyncMediaService(
    AsyncMediaMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/integration/extensions/EXT-001/media"
    _model_class = DummyModel
    _collection_key = "data"


@pytest.fixture
def media_service(http_client):
    return DummyMediaService(http_client=http_client)


@pytest.fixture
def async_media_service(async_http_client):
    return DummyAsyncMediaService(http_client=async_http_client)


def test_upload_image(media_service, tmp_path) -> None:  # noqa: WPS210
    media_id = "MED-001"
    expected_response = {"id": media_id, "filename": "photo.jpg"}
    image_path = tmp_path / "photo.jpg"
    image_path.write_bytes(b"fake jpeg data")
    with image_path.open("rb") as image_file, respx.mock:
        mock_route = respx.put(
            f"https://api.example.com/public/v1/integration/extensions/EXT-001/media/{media_id}/image"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=expected_response,
            )
        )

        result = media_service.upload_image(media_id, image_file)

    assert mock_route.call_count == 1
    assert mock_route.calls[0].request.method == "PUT"
    assert result.to_dict() == expected_response
    assert isinstance(result, DummyModel)


async def test_async_upload_image(async_media_service, tmp_path) -> None:  # noqa: WPS210
    media_id = "MED-002"
    expected_response = {"id": media_id, "filename": "photo.jpg"}
    image_path = tmp_path / "photo.jpg"
    image_path.write_bytes(b"fake jpeg data")
    with image_path.open("rb") as image_file, respx.mock:
        mock_route = respx.put(
            f"https://api.example.com/public/v1/integration/extensions/EXT-001/media/{media_id}/image"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=expected_response,
            )
        )

        result = await async_media_service.upload_image(media_id, image_file)

    assert mock_route.call_count == 1
    assert mock_route.calls[0].request.method == "PUT"
    assert result.to_dict() == expected_response
    assert isinstance(result, DummyModel)
