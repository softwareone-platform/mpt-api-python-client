import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.catalog.products_media import (
    AsyncMediaService,
    Media,
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


@pytest.fixture
def media_data():
    return {
        "id": "MED-001",
        "name": "Product Screenshot",
        "type": "Image",
        "description": "Main product screenshot",
        "status": "Active",
        "filename": "screenshot.png",
        "size": 512000,
        "contentType": "image/png",
        "displayOrder": 1,
        "url": "https://example.com/screenshot.png",
        "product": {"id": "PRD-001", "name": "My Product"},
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_endpoint(media_service) -> None:
    result = media_service.path == "/public/v1/catalog/products/PRD-001/media"

    assert result is True


def test_async_endpoint(async_media_service) -> None:
    result = async_media_service.path == "/public/v1/catalog/products/PRD-001/media"

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "delete", "update", "download", "review", "publish", "unpublish", "iterate"],
)
def test_methods_present(media_service, method: str) -> None:
    result = hasattr(media_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "delete", "update", "download", "review", "publish", "unpublish", "iterate"],
)
def test_async_methods_present(async_media_service, method: str) -> None:
    result = hasattr(async_media_service, method)

    assert result is True


def test_media_primitive_fields(media_data):
    result = Media(media_data)

    assert result.to_dict() == media_data


def test_media_nested_fields_are_base_models(media_data):
    result = Media(media_data)

    assert isinstance(result.product, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_media_optional_fields_absent():
    result = Media({"id": "MED-001"})

    assert result.id == "MED-001"
    assert not hasattr(result, "name")
    assert not hasattr(result, "status")
    assert not hasattr(result, "audit")
