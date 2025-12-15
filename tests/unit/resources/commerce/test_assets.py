import pytest

from mpt_api_client.resources.commerce.assets import AssetService, AsyncAssetService


@pytest.fixture
def assets_service(http_client):
    return AssetService(http_client=http_client)


@pytest.fixture
def async_assets_service(async_http_client):
    return AsyncAssetService(http_client=async_http_client)


@pytest.mark.parametrize("method", ["create", "update", "get", "render", "terminate"])
def test_assets_service_methods(assets_service, method):
    result = hasattr(assets_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["create", "update", "get", "render", "terminate"])
def test_async_assets_service_methods(async_assets_service, method):
    result = hasattr(async_assets_service, method)

    assert result is True
