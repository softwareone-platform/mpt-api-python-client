import httpx
import pytest
import respx

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.extensibility.extensions import (
    AsyncExtensionsService,
    Extension,
    ExtensionsService,
)


@pytest.fixture
def extensions_service(http_client):
    return ExtensionsService(http_client=http_client)


@pytest.fixture
def async_extensions_service(async_http_client):
    return AsyncExtensionsService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "create",
        "update",
        "delete",
        "publish",
        "unpublish",
        "regenerate",
        "token",
        "download_icon",
        "iterate",
    ],
)
def test_mixins_present(extensions_service, method):
    result = hasattr(extensions_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "create",
        "update",
        "delete",
        "publish",
        "unpublish",
        "regenerate",
        "token",
        "download_icon",
        "iterate",
    ],
)
def test_async_mixins_present(async_extensions_service, method):
    result = hasattr(async_extensions_service, method)

    assert result is True


def test_extension_create(extensions_service, tmp_path):
    extension_data = {"name": "My Extension", "shortDescription": "A test extension"}
    expected_response = {"id": "EXT-001", "name": "My Extension"}
    icon_path = tmp_path / "icon.png"
    icon_path.write_bytes(b"fake image data")
    with icon_path.open("rb") as icon_file, respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/extensibility/extensions").mock(
            return_value=httpx.Response(httpx.codes.CREATED, json=expected_response)
        )

        result = extensions_service.create(extension_data, file=icon_file)

    assert mock_route.call_count == 1
    assert mock_route.calls[0].request.method == "POST"
    assert result.to_dict() == expected_response


async def test_async_extension_create(async_extensions_service, tmp_path):
    extension_data = {"name": "Async Extension", "shortDescription": "An async test extension"}
    expected_response = {"id": "EXT-002", "name": "Async Extension"}
    icon_path = tmp_path / "icon.png"
    icon_path.write_bytes(b"fake image data")
    with icon_path.open("rb") as icon_file, respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/extensibility/extensions").mock(
            return_value=httpx.Response(httpx.codes.CREATED, json=expected_response)
        )

        result = await async_extensions_service.create(extension_data, file=icon_file)

    assert mock_route.call_count == 1
    assert mock_route.calls[0].request.method == "POST"
    assert result.to_dict() == expected_response


def test_extension_update(extensions_service, tmp_path):
    extension_id = "EXT-001"
    update_data = {"name": "Updated Extension"}
    expected_response = {"id": extension_id, "name": "Updated Extension"}
    icon_path = tmp_path / "icon.png"
    icon_path.write_bytes(b"new icon data")
    with icon_path.open("rb") as icon_file, respx.mock:
        mock_route = respx.put(
            f"https://api.example.com/public/v1/extensibility/extensions/{extension_id}"
        ).mock(return_value=httpx.Response(httpx.codes.OK, json=expected_response))

        result = extensions_service.update(extension_id, update_data, file=icon_file)

    assert mock_route.call_count == 1
    assert mock_route.calls[0].request.method == "PUT"
    assert result.to_dict() == expected_response


async def test_async_extension_update(async_extensions_service, tmp_path):
    extension_id = "EXT-002"
    update_data = {"name": "Async Updated Extension"}
    expected_response = {"id": extension_id, "name": "Async Updated Extension"}
    icon_path = tmp_path / "icon.png"
    icon_path.write_bytes(b"new async icon data")
    with icon_path.open("rb") as icon_file, respx.mock:
        mock_route = respx.put(
            f"https://api.example.com/public/v1/extensibility/extensions/{extension_id}"
        ).mock(return_value=httpx.Response(httpx.codes.OK, json=expected_response))

        result = await async_extensions_service.update(extension_id, update_data, file=icon_file)

    assert mock_route.call_count == 1
    assert mock_route.calls[0].request.method == "PUT"
    assert result.to_dict() == expected_response


@pytest.fixture
def extension_data():
    return {
        "id": "EXT-001",
        "name": "My Extension",
        "icon": "https://example.com/icon.png",
        "revision": 1,
        "status": "Draft",
        "website": "https://example.com",
        "shortDescription": "Short description",
        "longDescription": "Long description",
        "vendor": {"id": "ACC-001", "name": "Vendor"},
        "categories": [{"id": "CAT-001", "name": "Category"}],
        "modules": [{"id": "MOD-001", "name": "Module"}],
        "statistics": {"installations": 5},
        "configuration": {"key": "value"},
        "meta": {"id": "META-001"},
        "service": {"url": "https://service.example.com"},
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_extension_primitive_fields(extension_data):
    result = Extension(extension_data)

    assert result.id == "EXT-001"
    assert result.name == "My Extension"
    assert result.revision == 1
    assert result.status == "Draft"
    assert result.website == "https://example.com"


def test_extension_nested_fields_are_base_models(extension_data):
    result = Extension(extension_data)

    assert isinstance(result.vendor, BaseModel)
    assert isinstance(result.statistics, BaseModel)
    assert isinstance(result.configuration, BaseModel)
    assert isinstance(result.meta, BaseModel)
    assert isinstance(result.service, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_extension_optional_fields_absent():
    result = Extension({"id": "EXT-001"})

    assert result.id == "EXT-001"
    assert not hasattr(result, "name")
    assert not hasattr(result, "status")
    assert not hasattr(result, "audit")
