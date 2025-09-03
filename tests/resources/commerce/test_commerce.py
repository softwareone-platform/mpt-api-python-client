from mpt_api_client.http import AsyncHTTPClient
from mpt_api_client.resources.commerce import AsyncCommerce, Commerce
from mpt_api_client.resources.commerce.agreements import AgreementsService, AsyncAgreementsService
from mpt_api_client.resources.commerce.orders import AsyncOrdersService, OrdersService


def test_commerce_init(http_client):
    commerce = Commerce(http_client=http_client)

    assert isinstance(commerce, Commerce)
    assert commerce.http_client is http_client


def test_commerce_orders_property(http_client):
    commerce = Commerce(http_client=http_client)

    orders_service = commerce.orders

    assert isinstance(orders_service, OrdersService)
    assert orders_service.http_client is http_client


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


def test_async_commerce_orders_property(async_http_client: AsyncHTTPClient):
    commerce = AsyncCommerce(http_client=async_http_client)

    orders_service = commerce.orders

    assert isinstance(orders_service, AsyncOrdersService)
    assert orders_service.http_client is async_http_client


def test_async_commerce_orders_multiple_calls(async_http_client: AsyncHTTPClient):
    commerce = AsyncCommerce(http_client=async_http_client)

    orders_service = commerce.orders
    orders_service_additional = commerce.orders

    assert orders_service is not orders_service_additional
    assert isinstance(orders_service, AsyncOrdersService)
    assert isinstance(orders_service_additional, AsyncOrdersService)


def test_async_agreements(async_http_client):
    commerce = AsyncCommerce(http_client=async_http_client)

    agreements = commerce.agreements

    assert isinstance(agreements, AsyncAgreementsService)
    assert agreements.http_client is async_http_client


def test_agreements(http_client):
    commerce = Commerce(http_client=http_client)

    agreements = commerce.agreements

    assert isinstance(agreements, AgreementsService)
    assert agreements.http_client is http_client
