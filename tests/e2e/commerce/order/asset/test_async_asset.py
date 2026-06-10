from contextlib import asynccontextmanager

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


async def _delete_order_asset(resource_manager, resource):
    try:
        await resource_manager.delete(resource.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete order asset: {getattr(error, 'title', str(error))}")  # noqa: WPS421


@asynccontextmanager
async def async_create_fixture_resource_and_delete(resource_manager, resource_data):
    resource = await resource_manager.create(resource_data)

    try:
        yield resource
    finally:
        await _delete_order_asset(resource_manager, resource)


@pytest.fixture
async def created_order_asset(async_mpt_vendor, order_asset_factory, created_order):
    asset_data = order_asset_factory(created_order.to_dict())
    orders = async_mpt_vendor.commerce.orders
    assets = orders.assets(created_order.id)
    async with async_create_fixture_resource_and_delete(assets, asset_data) as asset:
        yield asset


async def test_get_order_asset_by_id(async_mpt_vendor, created_order, created_order_asset):
    asset_id = created_order_asset.id
    assets = async_mpt_vendor.commerce.orders.assets(created_order.id)

    result = await assets.get(asset_id)

    assert result is not None


async def test_list_order_assets(async_mpt_vendor, created_order, created_order_asset):
    limit = 10
    orders = async_mpt_vendor.commerce.orders
    assets = orders.assets(created_order.id)

    result = await assets.fetch_page(limit=limit)

    assert result is not None


async def test_get_order_asset_by_id_not_found(
    async_mpt_vendor, created_order, created_order_asset, invalid_asset_id
):
    orders = async_mpt_vendor.commerce.orders
    assets = orders.assets(created_order.id)

    with pytest.raises(MPTAPIError, match="404 Not Found"):
        await assets.get(invalid_asset_id)


async def test_filter_order_assets(async_mpt_vendor, created_order, created_order_asset):
    select_fields = ["-externalIds"]
    asset_id = created_order_asset.id
    assets = async_mpt_vendor.commerce.orders.assets(created_order.id)
    filtered_assets = (
        assets
        .filter(RQLQuery(id=asset_id))
        .filter(RQLQuery(name="E2E Created Order Asset"))
        .select(*select_fields)
    )

    result = [asset async for asset in filtered_assets.iterate()]

    assert len(result) == 1


def test_create_order_asset(created_order_asset):
    result = created_order_asset

    assert result is not None


async def test_update_order_asset(
    async_mpt_vendor,
    created_order,
    created_order_asset,
):
    asset_id = created_order_asset.id
    updated_asset_data = {
        "name": "E2E Updated Order Asset",
    }
    orders = async_mpt_vendor.commerce.orders
    assets = orders.assets(created_order.id)

    result = await assets.update(asset_id, updated_asset_data)

    assert result is not None


async def test_delete_order_asset(
    async_mpt_vendor,
    created_order,
    created_order_asset,
):
    asset_id = created_order_asset.id
    orders = async_mpt_vendor.commerce.orders

    result = orders.assets(created_order.id)

    await result.delete(asset_id)


async def test_render_order_asset(
    async_mpt_vendor,
    created_order,
    created_order_asset,
):
    asset_id = created_order_asset.id
    orders = async_mpt_vendor.commerce.orders
    assets = orders.assets(created_order.id)

    result = await assets.render(asset_id)

    assert result is not None
