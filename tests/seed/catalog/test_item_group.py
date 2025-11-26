from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.catalog.products_item_groups import AsyncItemGroupsService, ItemGroup
from seed.catalog.item_group import (
    build_item_group,
    get_item_group,
    init_item_group,
    seed_item_group,
    set_item_group,
)


@pytest.fixture
def item_group():
    return ItemGroup({
        "id": "group-123",
    })


@pytest.fixture
def item_group_service():
    return AsyncMock(spec=AsyncItemGroupsService)


@pytest.fixture
def vendor_client() -> AsyncMock:
    return MagicMock(spec=AsyncMPTClient)


@pytest.fixture
def mock_set_item_group(mocker):
    return mocker.patch("seed.catalog.item_group.set_item_group", spec=set_item_group)


async def test_get_item_group(context, vendor_client, item_group, mock_set_item_group) -> None:
    context["catalog.item_group.id"] = item_group.id
    context["catalog.product.id"] = "product-123"
    service = AsyncMock(spec=AsyncItemGroupsService)
    service.get.return_value = item_group
    vendor_client.catalog.products.item_groups.return_value = service
    mock_set_item_group.return_value = item_group

    result = await get_item_group(context=context, mpt_vendor=vendor_client)

    assert result == item_group
    service.get.assert_called_once_with(context["catalog.item_group.id"])
    service.create.assert_not_called()


async def test_get_item_group_without_id(context) -> None:
    result = await get_item_group(context=context)

    assert result is None


def test_set_item_group(context, item_group) -> None:
    result = set_item_group(item_group, context=context)

    assert result == item_group
    assert context.get("catalog.item_group.id") == "group-123"
    assert context.get("catalog.item_group[group-123]") == item_group


def test_build_item_group(context) -> None:
    context["catalog.product.id"] = "product-123"

    result = build_item_group(context=context)

    assert result["product"]["id"] == "product-123"


async def test_get_or_create_item_group_create_new(
    context, vendor_client, item_group_service, item_group
) -> None:
    context["catalog.product.id"] = "product-123"
    item_group_service.create.return_value = item_group
    vendor_client.catalog.products.item_groups.return_value = item_group_service

    with (
        patch("seed.catalog.item_group.get_item_group", return_value=None),
        patch("seed.catalog.item_group.build_item_group", return_value=item_group),
        patch("seed.catalog.item_group.set_item_group", return_value=item_group) as set_item_group,
    ):
        result = await init_item_group(context=context, mpt_vendor=vendor_client)

        assert result == item_group
        set_item_group.assert_called_once_with(item_group)
        item_group_service.create.assert_called_once()


async def test_seed_item_group() -> None:
    with patch("seed.catalog.item_group.init_item_group", new_callable=AsyncMock) as mock_create:
        await seed_item_group()  # act

        mock_create.assert_called_once()
