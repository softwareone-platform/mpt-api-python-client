import httpx
import pytest
import respx

from mpt_api_client.http.async_service import AsyncService
from mpt_api_client.http.service import Service
from mpt_api_client.models import FileModel
from mpt_api_client.resources.extensibility.mixins import (
    AsyncExtensionMixin,
    ExtensionMixin,
)
from tests.unit.conftest import DummyModel


class DummyExtensionService(
    ExtensionMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/extensibility/extensions"
    _model_class = DummyModel
    _collection_key = "data"


class DummyAsyncExtensionService(
    AsyncExtensionMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/extensibility/extensions"
    _model_class = DummyModel
    _collection_key = "data"


@pytest.fixture
def extension_service(http_client):
    return DummyExtensionService(http_client=http_client)


@pytest.fixture
def async_extension_service(async_http_client):
    return DummyAsyncExtensionService(http_client=async_http_client)


@pytest.mark.parametrize(
    "action",
    ["publish", "unpublish", "regenerate", "token"],
)
def test_post_actions(extension_service, action):
    extension_id = "EXT-001"
    expected_response = {"id": extension_id, "status": "updated"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/extensibility/extensions/{extension_id}/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=expected_response,
            )
        )

        result = getattr(extension_service, action)(extension_id)

        assert mock_route.call_count == 1
        assert mock_route.calls[0].request.method == "POST"
        assert result.to_dict() == expected_response
        assert isinstance(result, DummyModel)


def test_download_icon(extension_service):
    extension_id = "EXT-001"
    icon_bytes = b"\x89PNG\r\n\x1a\n"
    with respx.mock:
        mock_route = respx.get(
            f"https://api.example.com/public/v1/extensibility/extensions/{extension_id}/icon"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "image/png"},
                content=icon_bytes,
            )
        )

        result = extension_service.download_icon(extension_id)

        assert mock_route.call_count == 1
        assert mock_route.calls[0].request.method == "GET"
        assert isinstance(result, FileModel)
        assert result.file_contents == icon_bytes


@pytest.mark.parametrize(
    "action",
    ["publish", "unpublish", "regenerate", "token"],
)
async def test_async_post_actions(async_extension_service, action):
    extension_id = "EXT-001"
    expected_response = {"id": extension_id, "status": "updated"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/extensibility/extensions/{extension_id}/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=expected_response,
            )
        )

        result = await getattr(async_extension_service, action)(extension_id)

        assert mock_route.call_count == 1
        assert mock_route.calls[0].request.method == "POST"
        assert result.to_dict() == expected_response
        assert isinstance(result, DummyModel)


async def test_async_download_icon(async_extension_service):
    extension_id = "EXT-001"
    icon_bytes = b"\x89PNG\r\n\x1a\n"
    with respx.mock:
        mock_route = respx.get(
            f"https://api.example.com/public/v1/extensibility/extensions/{extension_id}/icon"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "image/png"},
                content=icon_bytes,
            )
        )

        result = await async_extension_service.download_icon(extension_id)

        assert mock_route.call_count == 1
        assert mock_route.calls[0].request.method == "GET"
        assert isinstance(result, FileModel)
        assert result.file_contents == icon_bytes
