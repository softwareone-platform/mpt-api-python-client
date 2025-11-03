import pytest

from mpt_api_client import AsyncMPTClient
from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def async_created_account(logger, async_mpt_ops, account, account_icon):
    account_data = account()

    res_account = await async_mpt_ops.accounts.accounts.create(account_data, logo=account_icon)

    yield res_account

    try:
        await async_mpt_ops.accounts.accounts.deactivate(res_account.id)
    except MPTAPIError as error:
        print("TEARDOWN - Unable to deactivate account: %s", error.title)  # noqa: WPS421


async def test_get_account_by_id_not_found(async_mpt_ops):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.accounts.get("INVALID-ID")


async def test_get_account_by_id(async_mpt_ops, account_id):
    account = await async_mpt_ops.accounts.accounts.get(account_id)
    assert account is not None


async def test_list_accounts(async_mpt_ops):
    limit = 10
    accounts_page = await async_mpt_ops.accounts.accounts.fetch_page(limit=limit)
    assert len(accounts_page) > 0


def test_create_account(async_created_account):
    account = async_created_account
    assert account is not None


async def test_update_account(async_mpt_ops, async_created_account, account, account_icon):
    updated_data = account(name="Updated Account Name")

    updated_account = await async_mpt_ops.accounts.accounts.update(
        async_created_account.id, updated_data, logo=account_icon
    )

    assert updated_account is not None


async def test_update_account_invalid_data(
    async_mpt_ops, account, async_created_account, account_icon
):
    updated_data = account(name="")

    with pytest.raises(MPTAPIError, match=r"400 Bad Request"):
        await async_mpt_ops.accounts.accounts.update(
            async_created_account.id, updated_data, logo=account_icon
        )


async def test_update_account_not_found(async_mpt_ops, account, invalid_account_id, account_icon):
    non_existent_account = account(name="Non Existent Account")

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.accounts.update(
            invalid_account_id, non_existent_account, logo=account_icon
        )


async def test_account_enable(async_mpt_ops, account, async_created_account):
    await async_mpt_ops.accounts.accounts.disable(async_created_account.id)

    account = await async_mpt_ops.accounts.accounts.enable(async_created_account.id)

    assert account is not None


async def test_account_enable_not_found(async_mpt_ops, invalid_account_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.accounts.enable(invalid_account_id)


async def test_account_disable(async_mpt_ops, async_created_account):
    account = await async_mpt_ops.accounts.accounts.disable(async_created_account.id)

    assert account is not None


async def test_account_disable_not_found(async_mpt_ops, invalid_account_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.accounts.disable(invalid_account_id)


async def test_account_rql_filter(async_mpt_ops, account_id):
    selected_fields = ["-address"]
    filtered_accounts = (
        async_mpt_ops.accounts.accounts.filter(RQLQuery(id=account_id))
        .filter(RQLQuery(name="Test Api Client Vendor"))
        .select(*selected_fields)
    )

    accounts = [account async for account in filtered_accounts.iterate()]

    assert len(accounts) > 0
