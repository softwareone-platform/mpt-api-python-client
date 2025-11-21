import pytest
import uuid

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_account_user(mpt_vendor, account_user_factory, account_id):
    ret_account_user = None

    def _created_account_user(
        first_name: str = "E2E Created",
        last_name: str = "Account User",
    ):
        nonlocal ret_account_user  # noqa: WPS420
        account_user_data = account_user_factory(
            first_name=first_name,
            last_name=last_name,
        )
        ret_account_user = (
            mpt_vendor.accounts.accounts.users(account_id=account_id).create(account_user_data)
        )
        return ret_account_user

    yield _created_account_user

    if ret_account_user:
        try:
            mpt_vendor.accounts.accounts.users(account_id=account_id).delete(ret_account_user.id)
        except MPTAPIError:
            print(  # noqa: WPS421
                f"TEARDOWN - Unable to delete account user {ret_account_user.id}",
            )


def test_get_account_user_by_id(mpt_vendor, user_id, account_id):
    account_user = mpt_vendor.accounts.accounts.users(account_id=account_id).get(user_id)
    assert account_user is not None


def test_list_account_users(mpt_vendor, account_id):
    limit = 10

    account_users = mpt_vendor.accounts.accounts.users(account_id=account_id).fetch_page(limit=limit)

    assert len(account_users) > 0


def test_get_account_user_by_id_not_found(mpt_vendor, invalid_user_id, account_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_vendor.accounts.accounts.users(account_id=account_id).get(invalid_user_id)


def test_filter_account_users(mpt_vendor, user_id, account_id):
    select_fields = ["-name"]

    filtered_account_users = (
        mpt_vendor.accounts.accounts.users(account_id=account_id).filter(RQLQuery(id=user_id))
        .select(*select_fields)
    )

    account_users = list(filtered_account_users.iterate())

    assert len(account_users) == 1


def test_create_account_user(created_account_user):
    account_user_data = created_account_user()
    assert account_user_data is not None


def test_delete_account_user(mpt_vendor, created_account_user, account_id):
    account_user_data = created_account_user()
    mpt_vendor.accounts.accounts.users(account_id=account_id).delete(account_user_data.id)


def test_update_account_user(
    mpt_vendor,
    account_user_factory,
    created_account_user,
    account_id,
):
    account_user_data = created_account_user()
    updated_account_user_data = account_user_factory(
        first_name="E2E Updated",
        last_name="Account User",
    )
    updated_account_user = mpt_vendor.accounts.accounts.users(account_id=account_id).update(
        account_user_data.id,
        updated_account_user_data,
    )
    assert updated_account_user is not None


def test_account_user_resend_invite(
    mpt_vendor,
    created_account_user,
    account_id,
):
    account_user_data = created_account_user()
    resend_invite = (
        mpt_vendor.accounts.accounts.users(account_id=account_id).resend_invite(account_user_data.id)
    )
    assert resend_invite is not None
