import httpx
import pytest
import respx

from mpt_api_client.resources.catalog.product_terms import (
    AsyncTermService,
    TermService,
)
from mpt_api_client.resources.catalog.products import AsyncProductsService, ProductsService
from mpt_api_client.resources.catalog.products_documents import (
    AsyncDocumentService,
    DocumentService,
)
from mpt_api_client.resources.catalog.products_item_groups import (
    AsyncItemGroupsService,
    ItemGroupsService,
)
from mpt_api_client.resources.catalog.products_media import (
    AsyncMediaService,
    MediaService,
)
from mpt_api_client.resources.catalog.products_parameter_groups import (
    AsyncParameterGroupsService,
    ParameterGroupsService,
)
from mpt_api_client.resources.catalog.products_parameters import (
    AsyncParametersService,
    ParametersService,
)
from mpt_api_client.resources.catalog.products_templates import (
    AsyncTemplatesService,
    TemplatesService,
)


@pytest.fixture
def products_service(http_client):
    return ProductsService(http_client=http_client)


@pytest.fixture
def async_products_service(async_http_client):
    return AsyncProductsService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "review", "publish", "unpublish", "update_settings"],
)
def test_mixins_present(products_service, method):
    assert hasattr(products_service, method)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "review", "publish", "unpublish", "update_settings"],
)
def test_async_mixins_present(async_products_service, method):
    assert hasattr(async_products_service, method)


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("item_groups", ItemGroupsService),
        ("parameter_groups", ParameterGroupsService),
        ("media", MediaService),
        ("documents", DocumentService),
        ("product_parameters", ParametersService),
        ("templates", TemplatesService),
        ("terms", TermService),
    ],
)
def test_property_services(products_service, service_method, expected_service_class):
    property_service = getattr(products_service, service_method)("PRD-001")

    assert isinstance(property_service, expected_service_class)
    assert property_service.endpoint_params == {"product_id": "PRD-001"}


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("item_groups", AsyncItemGroupsService),
        ("parameter_groups", AsyncParameterGroupsService),
        ("media", AsyncMediaService),
        ("documents", AsyncDocumentService),
        ("product_parameters", AsyncParametersService),
        ("templates", AsyncTemplatesService),
        ("terms", AsyncTermService),
    ],
)
def test_async_property_services(async_products_service, service_method, expected_service_class):
    property_service = getattr(async_products_service, service_method)("PRD-001")

    assert isinstance(property_service, expected_service_class)
    assert property_service.endpoint_params == {"product_id": "PRD-001"}


def test_update_settings(products_service):
    """Test updating product settings."""
    product_id = "PRD-001"
    settings_data = {"visibility": "public", "searchable": True, "featured": False}
    expected_response = {"id": product_id, "name": "Test Product", "settings": settings_data}

    with respx.mock:
        mock_route = respx.put(
            f"https://api.example.com/public/v1/catalog/products/{product_id}/settings"
        ).mock(return_value=httpx.Response(httpx.codes.OK, json=expected_response))

        product = products_service.update_settings(product_id, settings_data)

    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "PUT"
    assert request.url.path == f"/public/v1/catalog/products/{product_id}/settings"
    assert product.to_dict() == expected_response


async def test_async_update_settings(async_products_service):
    """Test updating product settings asynchronously."""
    product_id = "PRD-002"
    settings_data = {"visibility": "private", "searchable": False, "featured": True}
    expected_response = {"id": product_id, "name": "Test Product Async", "settings": settings_data}

    with respx.mock:
        mock_route = respx.put(
            f"https://api.example.com/public/v1/catalog/products/{product_id}/settings"
        ).mock(return_value=httpx.Response(httpx.codes.OK, json=expected_response))

        product = await async_products_service.update_settings(product_id, settings_data)

    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "PUT"
    assert request.url.path == f"/public/v1/catalog/products/{product_id}/settings"
    assert product.to_dict() == expected_response


def test_product_create(products_service, tmp_path):
    """Test creating a product (sync)."""
    product_data = {"name": "New Product", "category": "Books"}
    expected_response = {"id": "PRD-123", "name": "New Product", "category": "Books"}

    # Create a temporary icon file
    icon_path = tmp_path / "icon.png"
    icon_path.write_bytes(b"fake image data")
    with icon_path.open("rb") as icon_file, respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/catalog/products").mock(
            return_value=httpx.Response(httpx.codes.CREATED, json=expected_response)
        )

        product = products_service.create(product_data, icon=icon_file)

    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "POST"
    assert request.url.path == "/public/v1/catalog/products"
    assert product.to_dict() == expected_response


async def test_async_product_create(async_products_service, tmp_path):
    """Test creating a product (async)."""
    product_data = {"name": "Async Product", "category": "Music"}
    expected_response = {"id": "PRD-456", "name": "Async Product", "category": "Music"}

    # Create a temporary icon file
    icon_path = tmp_path / "icon.png"
    icon_path.write_bytes(b"fake image data")
    with icon_path.open("rb") as icon_file, respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/catalog/products").mock(
            return_value=httpx.Response(httpx.codes.CREATED, json=expected_response)
        )

        product = await async_products_service.create(product_data, icon=icon_file)

    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "POST"
    assert request.url.path == "/public/v1/catalog/products"
    assert product.to_dict() == expected_response
