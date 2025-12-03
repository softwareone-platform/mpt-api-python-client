import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


async def test_get_user_by_id(async_mpt_vendor, user_id):
    """Test retrieving a user by ID."""
    users_service = async_mpt_vendor.accounts.users
    result = await users_service.get(user_id)
    assert result is not None


async def test_get_user_by_invalid_id(async_mpt_vendor, invalid_user_id):
    """Test retrieving a user by an invalid ID."""
    users_service = async_mpt_vendor.accounts.users
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await users_service.get(invalid_user_id)


async def test_filter_account_users(async_mpt_vendor, user_id):
    """Test filtering users within an account."""
    select_fields = ["-name"]
    users_service = async_mpt_vendor.accounts.users
    filtered_users = users_service.filter(RQLQuery(id=user_id)).select(*select_fields)
    result = [user async for user in filtered_users.iterate()]
    assert len(result) == 1


async def test_update_user(async_mpt_ops, async_created_account_user, user_factory, account_icon):
    """Test updating a user."""
    created_user = await async_created_account_user()
    updated_data = user_factory(
        first_name="E2E Updated",
        last_name="User",
    )
    users_service = async_mpt_ops.accounts.users
    result = await users_service.update(created_user.id, updated_data, file=account_icon)
    assert result.first_name == "E2E Updated"
    assert result.last_name == "User"


async def test_update_user_not_found(async_mpt_vendor, invalid_user_id, user_factory, account_icon):
    """Test updating a user that does not exist."""
    updated_data = user_factory(
        first_name="E2E Updated",
        last_name="User",
    )
    users_service = async_mpt_vendor.accounts.users
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await users_service.update(invalid_user_id, updated_data, file=account_icon)


async def test_user_block(async_mpt_ops, async_created_account_user):
    """Test blocking a user."""
    created_user = await async_created_account_user()
    users_service = async_mpt_ops.accounts.users
    result = await users_service.block(created_user.id)
    assert result is not None


async def test_user_unblock(async_mpt_ops, async_created_account_user):
    """Test unblocking a user."""
    created_user = await async_created_account_user()
    users_service = async_mpt_ops.accounts.users
    await users_service.block(created_user.id)
    result = await users_service.unblock(created_user.id)
    assert result is not None
