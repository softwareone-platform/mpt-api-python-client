from typing import Any

import pytest

from mpt_api_client.resources.catalog.products_parameter_groups import (
    AsyncParameterGroupsService,
    ParameterGroupsService,
)


@pytest.fixture
def parameter_groups_service(http_client: Any) -> ParameterGroupsService:
    return ParameterGroupsService(
        http_client=http_client, endpoint_params={"product_id": "PRD-001"}
    )


@pytest.fixture
def async_parameter_groups_service(async_http_client: Any) -> AsyncParameterGroupsService:
    return AsyncParameterGroupsService(
        http_client=async_http_client, endpoint_params={"product_id": "PRD-001"}
    )


def test_endpoint(parameter_groups_service):
    assert (
        parameter_groups_service.endpoint == "/public/v1/catalog/products/PRD-001/parameter-groups"
    )


def test_async_endpoint(async_parameter_groups_service):
    assert (
        async_parameter_groups_service.endpoint
        == "/public/v1/catalog/products/PRD-001/parameter-groups"
    )


@pytest.mark.parametrize("method", ["get", "create", "delete", "update"])
def test_methods_present(parameter_groups_service, method):
    assert hasattr(parameter_groups_service, method)


@pytest.mark.parametrize("method", ["get", "create", "delete", "update"])
def test_async_methods_present(async_parameter_groups_service, method):
    assert hasattr(async_parameter_groups_service, method)
