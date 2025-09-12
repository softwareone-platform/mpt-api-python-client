import pytest

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
    "method", ["get", "create", "update", "delete", "review", "publish", "unpublish"]
)
def test_mixins_present(products_service, method):
    assert hasattr(products_service, method)


@pytest.mark.parametrize(
    "method", ["get", "create", "update", "delete", "review", "publish", "unpublish"]
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
