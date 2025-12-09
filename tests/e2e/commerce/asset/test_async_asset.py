import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_asset(async_mpt_vendor, asset_factory):
    new_asset_request_data = asset_factory(
        name="E2E Created Asset",
    )

    result = await async_mpt_vendor.commerce.assets.create(new_asset_request_data)

    yield result

    try:
        await async_mpt_vendor.commerce.assets.terminate(result.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to terminate asset: {getattr(error, 'title', str(error))}")  # noqa: WPS421


async def test_get_asset_by_id(async_mpt_vendor, agreement_asset_id):
    result = await async_mpt_vendor.commerce.assets.get(agreement_asset_id)

    assert result is not None


async def test_list_assets(async_mpt_vendor):
    limit = 10

    result = await async_mpt_vendor.commerce.assets.fetch_page(limit=limit)

    assert len(result) > 0


async def test_get_asset_by_id_not_found(async_mpt_vendor, invalid_agreement_asset_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_vendor.commerce.assets.get(invalid_agreement_asset_id)


async def test_filter_assets(async_mpt_vendor, agreement_asset_id):
    select_fields = ["-externalIds"]
    filtered_assets = (
        async_mpt_vendor.commerce.assets.filter(RQLQuery(id=agreement_asset_id))
        .filter(RQLQuery(name="E2E Seeded Order Asset"))
        .select(*select_fields)
    )

    result = [asset async for asset in filtered_assets.iterate()]

    assert len(result) == 1


def test_create_asset(created_asset):
    result = created_asset

    assert result is not None


async def test_update_asset(async_mpt_vendor, created_asset):
    updated_asset_data = {
        "name": "E2E Updated Asset",
        "parameters": {"fulfillment": []},
    }

    result = await async_mpt_vendor.commerce.assets.update(created_asset.id, updated_asset_data)

    assert result is not None


async def test_terminate_asset(async_mpt_vendor, created_asset):
    result = await async_mpt_vendor.commerce.assets.terminate(created_asset.id)

    assert result is not None


async def test_render_asset(async_mpt_vendor, created_asset):
    result = await async_mpt_vendor.commerce.assets.render(created_asset.id)

    assert result is not None
