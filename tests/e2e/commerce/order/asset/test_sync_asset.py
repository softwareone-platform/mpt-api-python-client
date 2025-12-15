from contextlib import contextmanager

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@contextmanager
def create_fixture_resource_and_delete(resource_manager, resource_data):
    resource = resource_manager.create(resource_data)

    yield resource

    try:
        resource_manager.delete(resource.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete order asset: {getattr(error, 'title', str(error))}")  # noqa: WPS421


@pytest.fixture
def created_order_asset(mpt_vendor, order_asset_factory, commerce_asset_draft_order_id):
    # Must use this fixture for all tests to prevent api errors
    asset_data = order_asset_factory()
    orders = mpt_vendor.commerce.orders
    assets = orders.assets(commerce_asset_draft_order_id)
    with create_fixture_resource_and_delete(assets, asset_data) as asset:
        yield asset


def test_get_order_asset_by_id(mpt_vendor, created_order_asset, commerce_asset_draft_order_id):
    asset_id = created_order_asset.id
    orders = mpt_vendor.commerce.orders.assets(commerce_asset_draft_order_id)

    result = orders.get(asset_id)

    assert result is not None


def test_list_order_assets(mpt_vendor, created_order_asset, commerce_asset_draft_order_id):
    limit = 10
    orders = mpt_vendor.commerce.orders
    assets = orders.assets(commerce_asset_draft_order_id)

    result = assets.fetch_page(limit=limit)

    assert result is not None


def test_get_order_asset_by_id_not_found(
    mpt_vendor, created_order_asset, commerce_asset_draft_order_id, invalid_asset_id
):
    orders = mpt_vendor.commerce.orders
    assets = orders.assets(commerce_asset_draft_order_id)

    with pytest.raises(MPTAPIError, match="404 Not Found"):
        assets.get(invalid_asset_id)


def test_filter_order_assets(mpt_vendor, created_order_asset, commerce_asset_draft_order_id):
    select_fields = ["-externalIds"]
    asset_id = created_order_asset.id
    assets = mpt_vendor.commerce.orders.assets(commerce_asset_draft_order_id)
    filtered_assets = (
        assets.filter(RQLQuery(id=asset_id))
        .filter(RQLQuery(name="E2E Created Order Asset"))
        .select(*select_fields)
    )

    result = list(filtered_assets.iterate())

    assert len(result) == 1


def test_create_order_asset(created_order_asset):
    result = created_order_asset

    assert result is not None


def test_update_order_asset(
    mpt_vendor,
    created_order_asset,
    commerce_asset_draft_order_id,
):
    asset_id = created_order_asset.id
    updated_asset_data = {
        "name": "E2E Updated Order Asset",
    }
    orders = mpt_vendor.commerce.orders
    assets = orders.assets(commerce_asset_draft_order_id)

    result = assets.update(asset_id, updated_asset_data)

    assert result is not None


def test_delete_order_asset(
    mpt_vendor,
    created_order_asset,
    commerce_asset_draft_order_id,
):
    asset_id = created_order_asset.id
    orders = mpt_vendor.commerce.orders

    result = orders.assets(commerce_asset_draft_order_id)

    result.delete(asset_id)


def test_render_order_asset(
    mpt_vendor,
    created_order_asset,
    commerce_asset_draft_order_id,
):
    asset_id = created_order_asset.id
    orders = mpt_vendor.commerce.orders
    assets = orders.assets(commerce_asset_draft_order_id)

    result = assets.render(asset_id)

    assert result is not None
