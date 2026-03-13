import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.catalog.items import AsyncItemsService, Item, ItemsService


@pytest.fixture
def items_service(http_client):
    return ItemsService(http_client=http_client)


@pytest.fixture
def async_items_service(async_http_client):
    return AsyncItemsService(http_client=async_http_client)


@pytest.fixture
def item_data():
    return {
        "id": "ITM-001",
        "name": "My Item",
        "description": "Item description",
        "externalIds": {"vendor": "ext-001"},
        "group": {"id": "GRP-001", "name": "Group"},
        "unit": {"id": "UOM-001", "name": "Each"},
        "terms": {"id": "TRM-001", "name": "Terms"},
        "quantityNotApplicable": False,
        "status": "Active",
        "product": {"id": "PRD-001", "name": "My Product"},
        "parameters": [{"id": "PRM-001", "name": "Param"}],
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "create",
        "update",
        "delete",
        "review",
        "publish",
        "unpublish",
        "iterate",
    ],
)
def test_mixins_present(items_service, method):
    result = hasattr(items_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "create",
        "update",
        "delete",
        "review",
        "publish",
        "unpublish",
        "iterate",
    ],
)
def test_async_mixins_present(async_items_service, method):
    result = hasattr(async_items_service, method)

    assert result is True


def test_item_primitive_fields(item_data):
    result = Item(item_data)

    assert result.to_dict() == item_data


def test_item_nested_base_models(item_data):
    result = Item(item_data)

    assert isinstance(result.external_ids, BaseModel)
    assert isinstance(result.group, BaseModel)
    assert isinstance(result.unit, BaseModel)
    assert isinstance(result.product, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_item_optional_fields_absent():
    result = Item({"id": "ITM-001"})

    assert result.id == "ITM-001"
    assert not hasattr(result, "name")
    assert not hasattr(result, "status")
    assert not hasattr(result, "audit")
