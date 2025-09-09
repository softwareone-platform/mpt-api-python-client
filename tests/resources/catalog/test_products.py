import pytest

from mpt_api_client.resources.catalog.products import AsyncProductsService, ProductsService
from mpt_api_client.resources.catalog.products_parameter_groups import (
    AsyncParameterGroupsService,
    ParameterGroupsService,
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


def test_parameters_groups_service(products_service):
    parameters_groups_service = products_service.parameter_groups("PRD-001")

    assert isinstance(parameters_groups_service, ParameterGroupsService)
    assert parameters_groups_service.endpoint_params == {"product_id": "PRD-001"}


def test_async_parameters_groups_service(async_products_service):
    parameters_groups_service = async_products_service.parameter_groups("PRD-001")

    assert isinstance(parameters_groups_service, AsyncParameterGroupsService)
    assert parameters_groups_service.endpoint_params == {"product_id": "PRD-001"}
