import pytest

from mpt_api_client.resources.catalog.products_parameters import (
    AsyncParametersService,
    ParametersService,
)


@pytest.fixture
def parameters_service(http_client):
    return ParametersService(http_client=http_client, endpoint_params={"product_id": "PRD-001"})


@pytest.fixture
def async_parameters_service(async_http_client):
    return AsyncParametersService(
        http_client=async_http_client, endpoint_params={"product_id": "PRD-001"}
    )


def test_endpoint(parameters_service):
    assert parameters_service.path == "/public/v1/catalog/products/PRD-001/parameters"


def test_async_endpoint(async_parameters_service):
    assert async_parameters_service.path == "/public/v1/catalog/products/PRD-001/parameters"


@pytest.mark.parametrize("method", ["get", "create", "delete", "update"])
def test_methods_present(parameters_service, method):
    assert hasattr(parameters_service, method)


@pytest.mark.parametrize("method", ["get", "create", "delete", "update"])
def test_async_methods_present(async_parameters_service, method):
    assert hasattr(async_parameters_service, method)
