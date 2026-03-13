import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.catalog.products_item_groups import (
    AsyncItemGroupsService,
    ItemGroup,
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


@pytest.fixture
def item_group_data():
    return {
        "id": "GRP-001",
        "name": "Standard Options",
        "label": "Standard",
        "description": "Standard option group",
        "displayOrder": 1,
        "default": True,
        "multiple": False,
        "required": True,
        "itemCount": 5,
        "product": {"id": "PRD-001", "name": "My Product"},
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_endpoint(item_groups_service):
    result = item_groups_service.path == "/public/v1/catalog/products/PRD-001/item-groups"

    assert result is True


def test_async_endpoint(async_item_groups_service):
    result = async_item_groups_service.path == "/public/v1/catalog/products/PRD-001/item-groups"

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "delete", "update", "iterate"])
def test_methods_present(item_groups_service, method):
    result = hasattr(item_groups_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "delete", "update", "iterate"])
def test_async_methods_present(async_item_groups_service, method):
    result = hasattr(async_item_groups_service, method)

    assert result is True


def test_item_group_primitive_fields(item_group_data):
    result = ItemGroup(item_group_data)

    assert result.to_dict() == item_group_data


def test_item_group_nested_fields_are_base_models(item_group_data):
    result = ItemGroup(item_group_data)

    assert isinstance(result.product, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_item_group_optional_fields_absent():
    result = ItemGroup({"id": "GRP-001"})

    assert result.id == "GRP-001"
    assert not hasattr(result, "name")
    assert not hasattr(result, "default")
    assert not hasattr(result, "audit")
