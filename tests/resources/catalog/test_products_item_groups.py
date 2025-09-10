import pytest

from mpt_api_client.resources.catalog.products_item_groups import (
    AsyncItemGroupsService,
    ItemGroupsService,
)


@pytest.fixture
def item_groups_service(http_client):
    return ItemGroupsService(http_client=http_client, endpoint_params={"product_id": "PRD-001"})


@pytest.fixture
def async_item_groups_service(async_http_client):
    return AsyncItemGroupsService(
        http_client=async_http_client, endpoint_params={"product_id": "PRD-001"}
    )


def test_endpoint(item_groups_service):
    assert item_groups_service.endpoint == "/public/v1/catalog/products/PRD-001/item-groups"


def test_async_endpoint(async_item_groups_service):
    assert async_item_groups_service.endpoint == "/public/v1/catalog/products/PRD-001/item-groups"


@pytest.mark.parametrize("method", ["get", "create", "delete", "update"])
def test_methods_present(item_groups_service, method):
    assert hasattr(item_groups_service, method)


@pytest.mark.parametrize("method", ["get", "create", "delete", "update"])
def test_async_methods_present(async_item_groups_service, method):
    assert hasattr(async_item_groups_service, method)
