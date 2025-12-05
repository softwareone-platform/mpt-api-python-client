import pytest

from mpt_api_client.resources.catalog.products_parameter_groups import (
    AsyncParameterGroupsService,
    ParameterGroupsService,
)


@pytest.fixture
def parameter_groups_service(http_client):
    return ParameterGroupsService(
        http_client=http_client, endpoint_params={"product_id": "PRD-001"}
    )


@pytest.fixture
def async_parameter_groups_service(async_http_client):
    return AsyncParameterGroupsService(
        http_client=async_http_client, endpoint_params={"product_id": "PRD-001"}
    )


def test_endpoint(parameter_groups_service):
    result = parameter_groups_service.path == "/public/v1/catalog/products/PRD-001/parameter-groups"

    assert result is True


def test_async_endpoint(async_parameter_groups_service):
    result = (
        async_parameter_groups_service.path
        == "/public/v1/catalog/products/PRD-001/parameter-groups"
    )

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "delete", "update", "iterate"])
def test_methods_present(parameter_groups_service, method):
    result = hasattr(parameter_groups_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "delete", "update", "iterate"])
def test_async_methods_present(async_parameter_groups_service, method):
    result = hasattr(async_parameter_groups_service, method)

    assert result is True
