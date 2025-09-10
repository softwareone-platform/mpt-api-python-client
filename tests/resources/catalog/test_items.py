from typing import Any

import pytest

from mpt_api_client.resources.catalog.items import AsyncItemsService, ItemsService


@pytest.fixture
def items_service(http_client: Any) -> ItemsService:
    return ItemsService(http_client=http_client)


@pytest.fixture
def async_items_service(async_http_client: Any) -> AsyncItemsService:
    return AsyncItemsService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method", ["get", "create", "update", "delete", "review", "publish", "unpublish"]
)
def test_mixins_present(items_service: ItemsService, method: str) -> None:
    assert hasattr(items_service, method)


@pytest.mark.parametrize(
    "method", ["get", "create", "update", "delete", "review", "publish", "unpublish"]
)
def test_async_mixins_present(async_items_service: AsyncItemsService, method: str) -> None:
    assert hasattr(async_items_service, method)
