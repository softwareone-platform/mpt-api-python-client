import httpx
import pytest
import respx

from mpt_api_client.constants import APPLICATION_JSON
from mpt_api_client.resources.commerce.assets import AssetService, AsyncAssetService


@pytest.fixture
def assets_service(http_client):
    return AssetService(http_client=http_client)


@pytest.fixture
def async_assets_service(async_http_client):
    return AsyncAssetService(http_client=async_http_client)


async def test_async_render(async_assets_service):
    render_response = {"id": "ASSET-123", "title": "Sample Asset"}
    with respx.mock:
        respx.get("https://api.example.com/public/v1/commerce/assets/ASSET-123/render").mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": APPLICATION_JSON},
                json=render_response,
            )
        )

        result = await async_assets_service.render("ASSET-123")

        assert result is not None


def test_render(assets_service):
    render_response = {"id": "ASSET-123", "title": "Sample Asset"}
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/commerce/assets/ASSET-123/render"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": APPLICATION_JSON},
                json=render_response,
            )
        )

        result = assets_service.render("ASSET-123")

        assert mock_route.called
        assert mock_route.call_count == 1
        assert result is not None


def test_terminate(assets_service):
    response_data = {"id": "ASSET-123", "status": "terminated"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/commerce/assets/ASSET-123/terminate"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": APPLICATION_JSON},
                json=response_data,
            )
        )

        result = assets_service.terminate("ASSET-123")

        assert mock_route.called
        assert mock_route.call_count == 1
        assert result is not None


async def test_async_terminate(async_assets_service):
    response_data = {"id": "ASSET-123", "status": "terminated"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/commerce/assets/ASSET-123/terminate"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": APPLICATION_JSON},
                json=response_data,
            )
        )

        result = await async_assets_service.terminate("ASSET-123")

        assert mock_route.called
        assert mock_route.call_count == 1
        assert result is not None


@pytest.mark.parametrize("method", ["create", "update", "get", "render", "terminate"])
def test_assets_service_methods(assets_service, method):
    result = hasattr(assets_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["create", "update", "get", "render", "terminate"])
def test_async_assets_service_methods(async_assets_service, method):
    result = hasattr(async_assets_service, method)

    assert result is True
