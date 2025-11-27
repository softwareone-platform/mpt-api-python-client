import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def users(mpt_vendor, account_id):
    return mpt_vendor.accounts.accounts.users(account_id=account_id)  # noqa: WPS204


@pytest.fixture
def created_account_user(mpt_vendor, account_user_factory, account_id):
    """Fixture to create and teardown an account user."""
    ret_account_user = None

    def _created_account_user(
        first_name: str = "E2E Created",
        last_name: str = "Account User",
    ):
        """Create an account user with the given first and last name."""
        nonlocal ret_account_user  # noqa: WPS420
        account_user_data = account_user_factory(
            first_name=first_name,
            last_name=last_name,
        )
        users_obj = mpt_vendor.accounts.accounts.users(account_id=account_id)
        ret_account_user = users_obj.create(account_user_data)
        return ret_account_user

    yield _created_account_user

    if ret_account_user:
        users_obj = mpt_vendor.accounts.accounts.users(account_id=account_id)
        try:
            users_obj.delete(ret_account_user.id)
        except MPTAPIError:
            print(  # noqa: WPS421
                f"TEARDOWN - Unable to delete account user {ret_account_user.id}",
            )


@pytest.fixture
def created_user_group(mpt_ops, user_group_factory):
    """Fixture to create and teardown a user group."""
    new_user_group_request_data = user_group_factory()
    created_user_group = mpt_ops.accounts.user_groups.create(new_user_group_request_data)

    yield created_user_group

    try:
        mpt_ops.accounts.user_groups.delete(created_user_group.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete user group: {error.title}")  # noqa: WPS421


@pytest.fixture
def created_account_user_group(mpt_vendor, created_account_user, created_user_group, account_id):  # noqa: WPS210
    """Fixture to create and teardown an account user group."""
    created_account_user_data = created_account_user()
    user_group_data = created_user_group
    create_user_group_data = {"id": user_group_data.id}
    users = mpt_vendor.accounts.accounts.users(account_id=account_id)
    created_account_user_group = users.groups(user_id=created_account_user_data.id).create(
        create_user_group_data
    )
    yield created_account_user_group

    users_obj = mpt_vendor.accounts.accounts.users(account_id=account_id)
    try:
        users_obj.groups(user_id=created_account_user_data.id).delete(user_group_data.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete account user group: {error.title}")  # noqa: WPS421


def test_get_account_user_by_id(mpt_vendor, user_id, account_id):
    """Test retrieving an account user by ID."""
    users_obj = mpt_vendor.accounts.accounts.users(account_id=account_id)

    result = users_obj.get(user_id)

    assert result is not None


def test_list_account_users(mpt_vendor, account_id):
    """Test listing account users."""
    limit = 10
    users_obj = mpt_vendor.accounts.accounts.users(account_id=account_id)

    result = users_obj.fetch_page(limit=limit)

    assert len(result) > 0


def test_get_account_user_by_id_not_found(mpt_vendor, invalid_user_id, account_id):
    """Test retrieving an account user by invalid ID."""
    users_obj = mpt_vendor.accounts.accounts.users(account_id=account_id)

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        users_obj.get(invalid_user_id)


def test_filter_account_users(mpt_vendor, user_id, account_id):
    """Test filtering account users."""
    select_fields = ["-name"]
    users_obj = mpt_vendor.accounts.accounts.users(account_id=account_id)
    filtered_account_users = users_obj.filter(RQLQuery(id=user_id)).select(*select_fields)

    result = list(filtered_account_users.iterate())

    assert len(result) == 1


def test_create_account_user(created_account_user):
    """Test creating an account user."""
    result = created_account_user()

    assert result is not None


def test_delete_account_user(mpt_vendor, created_account_user, account_id):
    """Test deleting an account user."""
    account_user_data = created_account_user()

    result = mpt_vendor.accounts.accounts.users(account_id=account_id)

    result.delete(account_user_data.id)


def test_update_account_user(
    mpt_vendor,
    account_user_factory,
    created_account_user,
    account_id,
):
    """Test updating an account user."""
    account_user_data = created_account_user()
    users_obj = mpt_vendor.accounts.accounts.users(account_id=account_id)
    updated_account_user_data = account_user_factory(
        first_name="E2E Updated",
        last_name="Account User",
    )

    result = users_obj.update(
        account_user_data.id,
        updated_account_user_data,
    )

    assert result is not None


def test_account_user_resend_invite(
    mpt_vendor,
    created_account_user,
    account_id,
):
    """Test resending an invite to an account user."""
    account_user_data = created_account_user()
    users_obj = mpt_vendor.accounts.accounts.users(account_id=account_id)

    result = users_obj.resend_invite(account_user_data.id)

    assert result is not None


def test_account_user_group_post(created_account_user_group):
    """Test creating an account user group."""
    result = created_account_user_group

    assert result is not None


def test_account_user_group_update(
    mpt_vendor,
    created_account_user,
    created_user_group,
    account_id,
):
    """Test updating an account user group."""
    created_account_user_data = created_account_user()
    users_obj = mpt_vendor.accounts.accounts.users(account_id=account_id)
    update_user_group_data = [{"id": created_user_group.id}]

    result = users_obj.groups(user_id=created_account_user_data.id).update(update_user_group_data)

    assert result is not None


def test_account_user_group_delete(
    mpt_vendor,
    created_account_user,
    created_user_group,
    account_id,
):
    """Test deleting an account user group."""
    created_account_user_data = created_account_user()
    users_obj = mpt_vendor.accounts.accounts.users(account_id=account_id)
    create_user_group_data = {"id": created_user_group.id}
    users_obj.groups(user_id=created_account_user_data.id).create(create_user_group_data)

    users_obj.groups(user_id=created_account_user_data.id).delete(created_user_group.id)  # act
