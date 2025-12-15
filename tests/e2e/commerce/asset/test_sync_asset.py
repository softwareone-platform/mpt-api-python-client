import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_asset(mpt_vendor, asset_factory):
    new_asset_request_data = asset_factory(
        name="E2E Created Asset",
    )

    result = mpt_vendor.commerce.assets.create(new_asset_request_data)

    yield result

    try:
        mpt_vendor.commerce.assets.terminate(result.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to terminate asset: {getattr(error, 'title', str(error))}")  # noqa: WPS421


def test_get_asset_by_id(mpt_vendor, asset_id):
    result = mpt_vendor.commerce.assets.get(asset_id)

    assert result is not None


def test_list_assets(mpt_vendor):
    limit = 10

    result = mpt_vendor.commerce.assets.fetch_page(limit=limit)

    assert len(result) > 0


def test_get_asset_by_id_not_found(mpt_vendor, invalid_asset_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_vendor.commerce.assets.get(invalid_asset_id)


def test_filter_assets(mpt_vendor, asset_id):
    select_fields = ["-externalIds"]
    filtered_assets = (
        mpt_vendor.commerce.assets.filter(RQLQuery(id=asset_id))
        .filter(RQLQuery(name="E2E Seeded Order Asset"))
        .select(*select_fields)
    )

    result = list(filtered_assets.iterate())

    assert len(result) == 1


def test_create_asset(created_asset):
    result = created_asset

    assert result is not None


def test_update_asset(mpt_vendor, created_asset):
    updated_asset_data = {
        "name": "E2E Updated Asset",
        "parameters": {"fulfillment": []},
    }

    result = mpt_vendor.commerce.assets.update(created_asset.id, updated_asset_data)

    assert result is not None


def test_terminate_asset(mpt_vendor, created_asset):
    result = mpt_vendor.commerce.assets.terminate(created_asset.id)

    assert result is not None


def test_render_asset(mpt_vendor, created_asset):
    result = mpt_vendor.commerce.assets.render(created_asset.id)

    assert result is not None
