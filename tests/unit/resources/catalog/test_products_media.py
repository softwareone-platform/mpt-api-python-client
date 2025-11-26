import pytest

from mpt_api_client.resources.catalog.products_media import (
    AsyncMediaService,
    MediaService,
)


@pytest.fixture
def media_service(http_client) -> MediaService:
    return MediaService(http_client=http_client, endpoint_params={"product_id": "PRD-001"})


@pytest.fixture
def async_media_service(async_http_client) -> AsyncMediaService:
    return AsyncMediaService(
        http_client=async_http_client, endpoint_params={"product_id": "PRD-001"}
    )


def test_endpoint(media_service) -> None:
    result = media_service.path == "/public/v1/catalog/products/PRD-001/media"

    assert result is True


def test_async_endpoint(async_media_service) -> None:
    result = async_media_service.path == "/public/v1/catalog/products/PRD-001/media"

    assert result is True


@pytest.mark.parametrize(
    "method", ["get", "create", "delete", "update", "download", "review", "publish", "unpublish"]
)
def test_methods_present(media_service, method: str) -> None:
    result = hasattr(media_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method", ["get", "create", "delete", "update", "download", "review", "publish", "unpublish"]
)
def test_async_methods_present(async_media_service, method: str) -> None:
    result = hasattr(async_media_service, method)

    assert result is True
