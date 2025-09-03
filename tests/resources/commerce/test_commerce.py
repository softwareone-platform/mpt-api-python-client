import pytest

from mpt_api_client.http import AsyncHTTPClient
from mpt_api_client.resources.commerce import AsyncCommerce, Commerce
from mpt_api_client.resources.commerce.agreements import AgreementsService, AsyncAgreementsService
from mpt_api_client.resources.commerce.orders import AsyncOrdersService, OrdersService
from mpt_api_client.resources.commerce.subscriptions import (
    AsyncSubscriptionsService,
    SubscriptionsService,
)


def test_commerce_init(http_client):
    commerce = Commerce(http_client=http_client)

    assert isinstance(commerce, Commerce)
    assert commerce.http_client is http_client


def test_commerce_orders_multiple_calls(http_client):
    commerce = Commerce(http_client=http_client)

    orders_service = commerce.orders
    order_service_additional = commerce.orders

    assert orders_service is not order_service_additional
    assert isinstance(orders_service, OrdersService)
    assert isinstance(order_service_additional, OrdersService)


def test_async_commerce_init(async_http_client: AsyncHTTPClient):
    commerce = AsyncCommerce(http_client=async_http_client)

    assert isinstance(commerce, AsyncCommerce)
    assert commerce.http_client is async_http_client


@pytest.mark.parametrize(
    ("attr_name", "expected"),
    [
        ("agreements", AgreementsService),
        ("orders", OrdersService),
        ("subscriptions", SubscriptionsService),
    ],
)
def test_commerce_properties(http_client, attr_name, expected):
    commerce = Commerce(http_client=http_client)

    service = getattr(commerce, attr_name)

    assert isinstance(service, expected)


@pytest.mark.parametrize(
    ("attr_name", "expected"),
    [
        ("agreements", AsyncAgreementsService),
        ("orders", AsyncOrdersService),
        ("subscriptions", AsyncSubscriptionsService),
    ],
)
def test_async_commerce_properties(http_client, attr_name, expected):
    commerce = AsyncCommerce(http_client=http_client)

    service = getattr(commerce, attr_name)

    assert isinstance(service, expected)
