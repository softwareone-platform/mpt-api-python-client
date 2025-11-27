from unittest.mock import AsyncMock, patch

import pytest

from mpt_api_client.resources.catalog.items import AsyncItemsService, Item
from seed.catalog.item import (
    create_item,
    get_item,
    publish_item,
    review_item,
    seed_items,
)
from seed.context import Context


@pytest.fixture
def resource_item() -> Item:  # noqa: WPS110
    return Item({"id": "item-123", "status": "Draft"})


@pytest.fixture
def items_service():
    return AsyncMock(spec=AsyncItemsService)


async def test_get_item(context: Context, vendor_client, resource_item) -> None:  # noqa: WPS110
    context["catalog.item.id"] = resource_item.id
    service = AsyncMock(spec=AsyncItemsService)
    service.get.return_value = resource_item
    vendor_client.catalog.items = service

    result = await get_item(context=context, mpt_vendor=vendor_client)

    assert result == resource_item
    assert context.get(f"catalog.item[{resource_item.id}]") == resource_item


async def test_get_item_without_id(context: Context) -> None:
    result = await get_item(context=context)

    assert result is None


async def test_create_item(context: Context, vendor_client, resource_item, items_service) -> None:  # noqa: WPS110
    items_service.create.return_value = resource_item
    vendor_client.catalog.items = items_service

    result = await create_item(context=context, mpt_vendor=vendor_client)

    assert result == resource_item
    assert context.get("catalog.item.id") == resource_item.id
    assert context.get(f"catalog.item[{resource_item.id}]") == resource_item


async def test_review_item_draft_status(
    context: Context, vendor_client, resource_item, items_service
) -> None:  # noqa: WPS110
    resource_item.status = "Draft"
    items_service.review.return_value = resource_item
    vendor_client.catalog.items = items_service
    context.set_resource("catalog.item", resource_item)
    context["catalog.item.id"] = resource_item.id

    result = await review_item(context=context, mpt_vendor=vendor_client)

    assert result == resource_item
    items_service.review.assert_called_once()


async def test_review_item_non_draft_status(
    context: Context, vendor_client, resource_item, items_service
) -> None:  # noqa: WPS110
    resource_item.status = "Published"
    items_service.review.return_value = resource_item
    vendor_client.catalog.items = items_service
    context.set_resource("catalog.item", resource_item)
    context["catalog.item.id"] = resource_item.id

    await review_item(context=context, mpt_vendor=vendor_client)  # act

    items_service.review.assert_not_called()


async def test_publish_item_reviewing_status(
    context: Context, operations_client, resource_item, items_service
) -> None:  # noqa: WPS110
    resource_item.status = "Reviewing"
    items_service.publish.return_value = resource_item
    operations_client.catalog.items = items_service
    context.set_resource("catalog.item", resource_item)
    context["catalog.item.id"] = resource_item.id

    result = await publish_item(context=context, mpt_operations=operations_client)

    assert result == resource_item
    operations_client.catalog.items.publish.assert_called_once()


async def test_publish_item_non_reviewing_status(
    context: Context, operations_client, resource_item, items_service
) -> None:  # noqa: WPS110
    resource_item.status = "Draft"
    items_service.publish.return_value = resource_item
    operations_client.catalog.items = items_service
    context.set_resource("catalog.item", resource_item)
    context["catalog.item.id"] = resource_item.id

    await publish_item(context=context, mpt_operations=operations_client)  # act

    operations_client.catalog.items.publish.assert_not_called()


async def test_seed_items(context: Context) -> None:
    with (
        patch(
            "seed.catalog.item.refresh_item", new_callable=AsyncMock, return_value=None
        ) as mock_refresh,
        patch("seed.catalog.item.create_item", new_callable=AsyncMock) as mock_create,
        patch("seed.catalog.item.review_item", new_callable=AsyncMock) as mock_review,
        patch("seed.catalog.item.publish_item", new_callable=AsyncMock) as mock_publish,
    ):
        await seed_items(context=context)  # act

        mock_refresh.assert_called_once()
        mock_create.assert_called_once()
        mock_review.assert_called_once()
        mock_publish.assert_called_once()
