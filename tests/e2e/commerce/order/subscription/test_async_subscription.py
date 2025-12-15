from contextlib import asynccontextmanager

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@asynccontextmanager
async def async_create_fixture_resource_and_delete(resource_manager, resource_data):
    resource = await resource_manager.create(resource_data)

    yield resource

    try:
        await resource_manager.delete(resource.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete subscription: {getattr(error, 'title', str(error))}")  # noqa: WPS421


@pytest.fixture
async def created_order_subscription(async_mpt_vendor, order_subscription_factory, order_id):
    # Must use this fixture for all tests to prevent api failures
    subscription_data = order_subscription_factory()
    orders = async_mpt_vendor.commerce.orders
    subscriptions = orders.subscriptions(order_id)
    async with async_create_fixture_resource_and_delete(
        subscriptions, subscription_data
    ) as subscription:
        yield subscription


async def test_get_order_subscription_by_id(async_mpt_vendor, created_order_subscription, order_id):
    subscription_id = created_order_subscription.id
    subscriptions = async_mpt_vendor.commerce.orders.subscriptions(order_id)

    result = await subscriptions.get(subscription_id)

    assert result is not None


async def test_list_order_subscriptions(async_mpt_vendor, created_order_subscription, order_id):
    limit = 10
    orders = async_mpt_vendor.commerce.orders
    subscriptions = orders.subscriptions(order_id)

    result = await subscriptions.fetch_page(limit=limit)

    assert result is not None


async def test_get_order_subscription_by_id_not_found(
    async_mpt_vendor, created_order_subscription, order_id, invalid_subscription_id
):
    orders = async_mpt_vendor.commerce.orders
    subscriptions = orders.subscriptions(order_id)

    with pytest.raises(MPTAPIError, match="404 Not Found"):
        await subscriptions.get(invalid_subscription_id)


async def test_filter_order_subscriptions(async_mpt_vendor, created_order_subscription, order_id):
    select_fields = ["-externalIds"]
    subscription_id = created_order_subscription.id
    subscriptions = async_mpt_vendor.commerce.orders.subscriptions(order_id)
    filtered_subscriptions = (
        subscriptions.filter(RQLQuery(id=subscription_id))
        .filter(RQLQuery(name="E2E Created Order Subscription"))
        .select(*select_fields)
    )

    result = [subscription async for subscription in filtered_subscriptions.iterate()]

    assert len(result) == 1


def test_create_order_subscription(created_order_subscription):
    result = created_order_subscription

    assert result is not None


async def test_update_order_subscription(async_mpt_vendor, created_order_subscription, order_id):
    subscription_id = created_order_subscription.id
    updated_subscription_data = {
        "name": "E2E Updated Order Subscription",
    }
    orders = async_mpt_vendor.commerce.orders
    subscriptions = orders.subscriptions(order_id)

    result = await subscriptions.update(subscription_id, updated_subscription_data)

    assert result is not None


async def test_delete_order_subscription(async_mpt_vendor, created_order_subscription, order_id):
    subscription_id = created_order_subscription.id
    orders = async_mpt_vendor.commerce.orders

    subscriptions = orders.subscriptions(order_id)
    await subscriptions.delete(subscription_id)
