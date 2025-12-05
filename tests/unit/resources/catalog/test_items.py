import pytest

from mpt_api_client.resources.catalog.items import AsyncItemsService, ItemsService


@pytest.fixture
def items_service(http_client):
    return ItemsService(http_client=http_client)


@pytest.fixture
def async_items_service(async_http_client):
    return AsyncItemsService(http_client=async_http_client)


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
