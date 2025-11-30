import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


def test_get_user_by_id(mpt_vendor, user_id):
    """Test retrieving a user by ID."""
    users_service = mpt_vendor.accounts.users

    result = users_service.get(user_id)

    assert result is not None


def test_get_user_by_invalid_id(mpt_vendor, invalid_user_id):
    """Test retrieving a user by an invalid ID."""
    users_service = mpt_vendor.accounts.users

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        users_service.get(invalid_user_id)


def test_filter_account_users(mpt_vendor, user_id):
    """Test filtering users within an account."""
    select_fields = ["-name"]
    users_service = mpt_vendor.accounts.users
    filtered_users = users_service.filter(RQLQuery(id=user_id)).select(*select_fields)

    result = list(filtered_users.iterate())

    assert len(result) == 1


def test_update_user(mpt_ops, created_account_user, user_factory, account_icon):
    """Test updating a user."""
    created_user = created_account_user()
    updated_data = user_factory(
        first_name="E2E Updated",
        last_name="User",
    )
    users_service = mpt_ops.accounts.users

    result = users_service.update(created_user.id, updated_data, file=account_icon)

    assert result.first_name == "E2E Updated"
    assert result.last_name == "User"


def test_update_user_not_found(mpt_vendor, invalid_user_id, user_factory, account_icon):
    """Test updating a user that does not exist."""
    updated_data = user_factory(
        first_name="E2E Updated",
        last_name="User",
    )
    users_service = mpt_vendor.accounts.users

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        users_service.update(invalid_user_id, updated_data, file=account_icon)


def test_user_block(mpt_ops, created_account_user):
    """Test blocking a user."""
    created_user = created_account_user()
    users_service = mpt_ops.accounts.users

    result = users_service.block(created_user.id)

    assert result is not None


def test_user_unblock(mpt_ops, created_account_user):
    """Test unblocking a user."""
    created_user = created_account_user()
    users_service = mpt_ops.accounts.users
    users_service.block(created_user.id)

    result = users_service.unblock(created_user.id)

    assert result is not None
