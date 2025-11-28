import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def async_created_account(logger, async_mpt_ops, account_factory, account_icon):
    """Fixture to create and yield an asynchronous account for testing."""
    account_data = account_factory()

    res_account = await async_mpt_ops.accounts.accounts.create(account_data, file=account_icon)

    yield res_account

    try:
        await async_mpt_ops.accounts.accounts.disable(res_account.id)
    except MPTAPIError as error:
        print("TEARDOWN - Unable to deactivate account: %s", error.title)  # noqa: WPS421


async def test_get_account_by_id_not_found(async_mpt_ops):
    """Test fetching an account by an invalid ID raises a 404 error."""
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.accounts.get("INVALID-ID")


async def test_get_account_by_id(async_mpt_ops, account_id):
    result = await async_mpt_ops.accounts.accounts.get(account_id)

    assert result is not None


async def test_list_accounts(async_mpt_ops):
    """Test listing accounts with a limit."""
    limit = 10

    result = await async_mpt_ops.accounts.accounts.fetch_page(limit=limit)

    assert len(result) > 0


def test_create_account(async_created_account):
    result = async_created_account

    assert result is not None


async def test_update_account(async_mpt_ops, async_created_account, account_factory, account_icon):
    """Test updating an account asynchronously."""
    updated_data = account_factory(name="Updated Account Name")

    result = await async_mpt_ops.accounts.accounts.update(
        async_created_account.id, updated_data, file=account_icon
    )

    assert result is not None


async def test_update_account_invalid_data(
    async_mpt_ops, account_factory, async_created_account, account_icon
):
    """Test updating an account with invalid data raises a 400 error."""
    updated_data = account_factory(name="")

    with pytest.raises(MPTAPIError, match=r"400 Bad Request"):
        await async_mpt_ops.accounts.accounts.update(
            async_created_account.id, updated_data, file=account_icon
        )


async def test_update_account_not_found(
    async_mpt_ops, account_factory, invalid_account_id, account_icon
):
    """Test updating a non-existent account raises a 404 error."""
    non_existent_account = account_factory(name="Non Existent Account")

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.accounts.update(
            invalid_account_id, non_existent_account, file=account_icon
        )


async def test_account_enable(async_mpt_ops, async_created_account):
    """Test enabling an account asynchronously."""
    await async_mpt_ops.accounts.accounts.disable(async_created_account.id)

    result = await async_mpt_ops.accounts.accounts.enable(async_created_account.id)

    assert result is not None


async def test_account_enable_not_found(async_mpt_ops, invalid_account_id):
    """Test enabling a non-existent account raises a 404 error."""
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.accounts.enable(invalid_account_id)


async def test_account_disable(async_mpt_ops, async_created_account):
    """Test disabling an account asynchronously."""
    result = await async_mpt_ops.accounts.accounts.disable(async_created_account.id)

    assert result is not None


async def test_account_disable_not_found(async_mpt_ops, invalid_account_id):
    """Test disabling a non-existent account raises a 404 error."""
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.accounts.disable(invalid_account_id)


async def test_account_rql_filter(async_mpt_ops, account_id):
    """Test filtering accounts using RQL asynchronously."""
    selected_fields = ["-address"]
    filtered_accounts = (
        async_mpt_ops.accounts.accounts.filter(RQLQuery(id=account_id))
        .filter(RQLQuery(name="Test Api Client Vendor"))
        .select(*selected_fields)
    )

    result = [account async for account in filtered_accounts.iterate()]

    assert len(result) > 0
