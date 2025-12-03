import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def users(async_mpt_vendor, account_id):
    return async_mpt_vendor.accounts.accounts.users(account_id=account_id)  # noqa: WPS204


@pytest.fixture
async def created_user_group(async_mpt_ops, user_group_factory):
    """Fixture to create and teardown a user group."""
    new_user_group_request_data = user_group_factory()
    created_user_group = await async_mpt_ops.accounts.user_groups.create(
        new_user_group_request_data
    )

    yield created_user_group

    try:
        await async_mpt_ops.accounts.user_groups.delete(created_user_group.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete user group: {getattr(error, 'title', str(error))}")  # noqa: WPS421


@pytest.fixture
async def created_account_user_group(  # noqa: WPS210
    async_mpt_vendor, async_created_account_user, created_user_group, account_id
):
    """Fixture to create and teardown an account user group."""
    created_account_user_data = await async_created_account_user()
    user_group_data = created_user_group
    create_user_group_data = {"id": user_group_data.id}
    users = async_mpt_vendor.accounts.accounts.users(account_id=account_id)
    created_account_user_group = await users.groups(user_id=created_account_user_data.id).create(
        create_user_group_data
    )
    yield created_account_user_group

    users_obj = async_mpt_vendor.accounts.accounts.users(account_id=account_id)
    try:
        await users_obj.groups(user_id=created_account_user_data.id).delete(user_group_data.id)
    except MPTAPIError as error:
        print(  # noqa: WPS421
            f"TEARDOWN - Unable to delete account user group: {getattr(error, 'title', str(error))}"
        )


async def test_get_account_user_by_id(async_mpt_vendor, user_id, account_id):
    """Test retrieving an account user by ID."""
    users_obj = async_mpt_vendor.accounts.accounts.users(account_id=account_id)

    account_user = await users_obj.get(user_id)

    assert account_user is not None


async def test_list_account_users(async_mpt_vendor, account_id):
    """Test listing account users."""
    limit = 10
    users_obj = async_mpt_vendor.accounts.accounts.users(account_id=account_id)

    result = await users_obj.fetch_page(limit=limit)

    assert len(result) > 0


async def test_get_account_user_by_id_not_found(async_mpt_vendor, invalid_user_id, account_id):
    """Test retrieving an account user by invalid ID."""
    result = async_mpt_vendor.accounts.accounts.users(account_id=account_id)

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await result.get(invalid_user_id)


async def test_filter_account_users(async_mpt_vendor, user_id, account_id):
    """Test filtering account users."""
    select_fields = ["-name"]
    users_obj = async_mpt_vendor.accounts.accounts.users(account_id=account_id)
    filtered_account_users = users_obj.filter(RQLQuery(id=user_id)).select(*select_fields)

    result = [user async for user in filtered_account_users.iterate()]

    assert len(result) == 1


async def test_create_account_user(async_created_account_user):
    """Test creating an account user."""
    result = await async_created_account_user()

    assert result is not None


async def test_delete_account_user(async_mpt_vendor, async_created_account_user, account_id):
    """Test deleting an account user."""
    account_user_data = await async_created_account_user()

    result = async_mpt_vendor.accounts.accounts.users(account_id=account_id)

    await result.delete(account_user_data.id)


async def test_update_account_user(
    async_mpt_vendor,
    account_user_factory,
    async_created_account_user,
    account_id,
):
    """Test updating an account user."""
    account_user_data = await async_created_account_user()

    users_obj = async_mpt_vendor.accounts.accounts.users(account_id=account_id)

    updated_account_user_data = account_user_factory(
        first_name="E2E Updated",
        last_name="Account User",
    )

    result = await users_obj.update(
        account_user_data.id,
        updated_account_user_data,
    )

    assert result is not None


async def test_account_user_resend_invite(
    async_mpt_vendor,
    async_created_account_user,
    account_id,
):
    """Test resending an invite to an account user."""
    account_user_data = await async_created_account_user()

    result = async_mpt_vendor.accounts.accounts.users(account_id=account_id)

    result = await result.resend_invite(account_user_data.id)

    assert result is not None


def test_account_user_group_post(created_account_user_group):  # noqa: AAA01
    """Test creating an account user group."""
    result = created_account_user_group

    assert result is not None


async def test_account_user_group_update(
    async_mpt_vendor,
    async_created_account_user,
    created_user_group,
    account_id,
):
    """Test updating an account user group."""
    created_account_user_data = await async_created_account_user()

    users_obj = async_mpt_vendor.accounts.accounts.users(account_id=account_id)

    update_user_group_data = [{"id": created_user_group.id}]

    result = await users_obj.groups(user_id=created_account_user_data.id).update(
        update_user_group_data
    )

    assert result is not None


async def test_account_user_group_delete(
    async_mpt_vendor,
    async_created_account_user,
    created_user_group,
    account_id,
):
    """Test deleting an account user group."""
    created_account_user_data = await async_created_account_user()

    users_obj = async_mpt_vendor.accounts.accounts.users(account_id=account_id)

    create_user_group_data = {"id": created_user_group.id}

    await users_obj.groups(user_id=created_account_user_data.id).create(create_user_group_data)

    await users_obj.groups(user_id=created_account_user_data.id).delete(created_user_group.id)
