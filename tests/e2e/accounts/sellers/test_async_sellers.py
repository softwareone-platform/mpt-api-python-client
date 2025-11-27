import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


# TODO: Handle create and teardown more gracefully with fixture that doesn't cause teardown issues
@pytest.fixture
async def async_created_seller(async_mpt_ops, seller_factory, logger):
    ret_seller = None

    async def _async_created_seller(
        external_id: str,
        name: str = "E2E Test Seller",
    ):
        nonlocal ret_seller  # noqa: WPS420
        seller_data = seller_factory(external_id=external_id, name=name)
        ret_seller = await async_mpt_ops.accounts.sellers.create(seller_data)
        return ret_seller

    yield _async_created_seller

    if ret_seller:
        try:
            await async_mpt_ops.accounts.sellers.delete(ret_seller.id)
        except MPTAPIError:
            print(f"TEARDOWN - Unable to delete seller {ret_seller.id}")  # noqa: WPS421


async def test_get_seller_by_id(async_mpt_ops, seller_id):
    result = await async_mpt_ops.accounts.sellers.get(seller_id)

    assert result is not None


async def test_list_sellers(async_mpt_ops):
    limit = 10

    result = await async_mpt_ops.accounts.sellers.fetch_page(limit=limit)

    assert len(result) > 0


async def test_get_seller_by_id_not_found(async_mpt_ops, invalid_seller_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.sellers.get(invalid_seller_id)


async def test_filter_sellers(async_mpt_ops, seller_id):
    select_fields = ["-address"]
    async_filtered_sellers = (
        async_mpt_ops.accounts.sellers.filter(RQLQuery(id=seller_id))
        .filter(RQLQuery(name="E2E Seeded Seller"))
        .select(*select_fields)
    )

    result = [filtered_seller async for filtered_seller in async_filtered_sellers.iterate()]

    assert len(result) == 1


async def test_create_seller(async_created_seller, timestamp):
    result = await async_created_seller(external_id=f"Async Create E2E Seller - {timestamp}")

    assert result is not None


async def test_delete_seller(async_mpt_ops, async_created_seller, timestamp):
    result = await async_created_seller(external_id=f"Async Delete E2E Seller - {timestamp}")

    await async_mpt_ops.accounts.sellers.delete(result.id)


async def test_delete_seller_not_found(async_mpt_ops, invalid_seller_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.sellers.delete(invalid_seller_id)


async def test_update_seller(async_mpt_ops, seller_factory, async_created_seller, timestamp):
    seller_data = await async_created_seller(external_id=f"Async Update E2E Seller - {timestamp}")
    update_data = seller_factory(
        external_id=f"Async Update E2E Seller - {timestamp}",
        name=f"Updated Update E2E Seller - {timestamp}",
    )

    result = await async_mpt_ops.accounts.sellers.update(seller_data.id, update_data)

    assert result is not None


async def test_update_seller_mpt_error(async_mpt_ops, seller_factory, timestamp, invalid_seller_id):
    update_data = seller_factory(
        external_id=f"Async Update E2E Seller Not Found - {timestamp}",
        name=f"Updated Update E2E Seller Not Found - {timestamp}",
    )

    with pytest.raises(MPTAPIError):
        await async_mpt_ops.accounts.sellers.update(invalid_seller_id, update_data)


async def test_activate_seller(async_mpt_ops, async_created_seller, timestamp):
    seller_data = await async_created_seller(external_id=f"Async Activate E2E Seller - {timestamp}")
    await async_mpt_ops.accounts.sellers.disable(seller_data.id)

    result = await async_mpt_ops.accounts.sellers.activate(seller_data.id)

    assert result is not None


async def test_activate_seller_mpt_error(async_mpt_ops, invalid_seller_id):
    with pytest.raises(MPTAPIError):
        await async_mpt_ops.accounts.sellers.activate(invalid_seller_id)


async def test_deactivate_seller(async_mpt_ops, async_created_seller, timestamp):
    seller_data = await async_created_seller(
        external_id=f"Async Deactivate E2E Seller - {timestamp}"
    )

    result = await async_mpt_ops.accounts.sellers.disable(seller_data.id)

    assert result is not None


async def test_deactivate_seller_mpt_error(async_mpt_ops, invalid_seller_id):
    with pytest.raises(MPTAPIError):
        await async_mpt_ops.accounts.sellers.disable(invalid_seller_id)


async def test_disable_seller(async_mpt_ops, async_created_seller, timestamp):
    seller_data = await async_created_seller(external_id=f"Async Disable E2E Seller - {timestamp}")

    result = await async_mpt_ops.accounts.sellers.disable(seller_data.id)

    assert result is not None


async def test_disable_seller_mpt_error(async_mpt_ops, invalid_seller_id):
    with pytest.raises(MPTAPIError):
        await async_mpt_ops.accounts.sellers.disable(invalid_seller_id)
