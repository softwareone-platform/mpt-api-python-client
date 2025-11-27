import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def async_created_buyer(async_mpt_ops, buyer_factory, buyer_account_id, account_icon):
    new_buyer_request_data = buyer_factory(
        name="E2E Created Buyer",
        account_id=buyer_account_id,
    )

    new_buyer = await async_mpt_ops.accounts.buyers.create(
        new_buyer_request_data, logo=account_icon
    )

    yield new_buyer

    try:
        await async_mpt_ops.accounts.buyers.delete(new_buyer.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete buyer: {error.title}")  # noqa: WPS421


async def test_get_buyer_by_id(async_mpt_ops, buyer_id):
    result = await async_mpt_ops.accounts.buyers.get(buyer_id)

    assert result is not None


async def test_list_buyers(async_mpt_ops):
    limit = 10

    result = await async_mpt_ops.accounts.buyers.fetch_page(limit=limit)

    assert len(result) > 0


async def test_get_buyer_by_id_not_found(async_mpt_ops, invalid_buyer_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.buyers.get(invalid_buyer_id)


async def test_filter_buyers(async_mpt_ops, buyer_id):
    select_fields = ["-address"]
    async_filtered_buyers = (
        async_mpt_ops.accounts.buyers.filter(RQLQuery(id=buyer_id))
        .filter(RQLQuery(name="E2E Seeded Buyer"))
        .select(*select_fields)
    )

    result = [filtered_buyer async for filtered_buyer in async_filtered_buyers.iterate()]

    assert len(result) == 1


def test_create_buyer(async_created_buyer):
    result = async_created_buyer

    assert result is not None


async def test_delete_buyer(async_mpt_ops, async_created_buyer):
    await async_mpt_ops.accounts.buyers.delete(async_created_buyer.id)  # act


async def test_delete_buyer_not_found(async_mpt_ops, invalid_buyer_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.buyers.delete(invalid_buyer_id)


async def test_update_buyer(
    async_mpt_ops, buyer_factory, buyer_account_id, account_icon, async_created_buyer
):
    updated_buyer_data = buyer_factory(name="E2E Updated Buyer", account_id=buyer_account_id)

    result = await async_mpt_ops.accounts.buyers.update(
        async_created_buyer.id, updated_buyer_data, logo=account_icon
    )

    assert result is not None


async def test_update_buyer_not_found(
    async_mpt_ops, buyer_factory, buyer_account_id, account_icon, invalid_buyer_id
):
    updated_buyer_data = buyer_factory(name="Nonexistent Buyer", account_id=buyer_account_id)

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.buyers.update(
            invalid_buyer_id, updated_buyer_data, logo=account_icon
        )


async def test_buyer_disable(async_mpt_ops, async_created_buyer):
    result = await async_mpt_ops.accounts.buyers.disable(async_created_buyer.id)

    assert result is not None


async def test_buyer_disable_not_found(async_mpt_ops, invalid_buyer_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.buyers.disable(invalid_buyer_id)


async def test_buyer_enable(async_mpt_ops, async_created_buyer):
    await async_mpt_ops.accounts.buyers.disable(async_created_buyer.id)

    result = await async_mpt_ops.accounts.buyers.enable(async_created_buyer.id)

    assert result is not None


async def test_buyer_enable_not_found(async_mpt_ops, invalid_buyer_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.buyers.enable(invalid_buyer_id)
