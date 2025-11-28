import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def async_created_buyer(async_mpt_ops, buyer_factory, buyer_account_id, account_icon):
    """Fixture to create and yield an asynchronous buyer for testing."""
    new_buyer_request_data = buyer_factory(
        name="E2E Created Buyer",
        account_id=buyer_account_id,
    )

    new_buyer = await async_mpt_ops.accounts.buyers.create(
        new_buyer_request_data, file=account_icon
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
    """Test listing buyers with a limit."""
    limit = 10

    result = await async_mpt_ops.accounts.buyers.fetch_page(limit=limit)

    assert len(result) > 0


async def test_get_buyer_by_id_not_found(async_mpt_ops, invalid_buyer_id):
    """Test fetching a buyer by an invalid ID raises a 404 error."""
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.buyers.get(invalid_buyer_id)


async def test_filter_buyers(async_mpt_ops, buyer_id):
    """Test filtering buyers using RQL asynchronously."""
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
    """Test deleting a non-existent buyer raises a 404 error."""
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.buyers.delete(invalid_buyer_id)


async def test_update_buyer(
    async_mpt_ops, buyer_factory, buyer_account_id, account_icon, async_created_buyer
):
    """Test updating a buyer asynchronously."""
    updated_buyer_data = buyer_factory(name="E2E Updated Buyer", account_id=buyer_account_id)

    result = await async_mpt_ops.accounts.buyers.update(
        async_created_buyer.id, updated_buyer_data, file=account_icon
    )

    assert result is not None


async def test_update_buyer_not_found(
    async_mpt_ops, buyer_factory, buyer_account_id, account_icon, invalid_buyer_id
):
    """Test updating a non-existent buyer raises a 404 error."""
    updated_buyer_data = buyer_factory(name="Nonexistent Buyer", account_id=buyer_account_id)

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.buyers.update(
            invalid_buyer_id, updated_buyer_data, file=account_icon
        )


async def test_buyer_disable(async_mpt_ops, async_created_buyer):
    result = await async_mpt_ops.accounts.buyers.disable(async_created_buyer.id)

    assert result is not None


async def test_buyer_disable_not_found(async_mpt_ops, invalid_buyer_id):
    """Test disabling a non-existent buyer raises a 404 error."""
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.buyers.disable(invalid_buyer_id)


async def test_buyer_enable(async_mpt_ops, async_created_buyer):
    """Test enabling a buyer asynchronously."""
    await async_mpt_ops.accounts.buyers.disable(async_created_buyer.id)

    result = await async_mpt_ops.accounts.buyers.enable(async_created_buyer.id)

    assert result is not None


async def test_buyer_enable_not_found(async_mpt_ops, invalid_buyer_id):
    """Test enabling a non-existent buyer raises a 404 error."""
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.buyers.enable(invalid_buyer_id)
