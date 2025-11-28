import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_account(mpt_ops, account_factory, account_icon):
    """Fixture to create and yield an account for testing."""
    account_data = account_factory()

    res_account = mpt_ops.accounts.accounts.create(account_data, file=account_icon)

    yield res_account

    try:
        mpt_ops.accounts.accounts.disable(res_account.id)
    except MPTAPIError as error:
        print("TEARDOWN - Unable to deactivate account: %s", error.title)  # noqa: WPS421


def test_get_account_by_id_not_found(mpt_ops):
    """Test fetching an account by an invalid ID raises a 404 error."""
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.accounts.accounts.get("INVALID-ID")


def test_get_account_by_id(mpt_ops, account_id):
    result = mpt_ops.accounts.accounts.get(account_id)

    assert result is not None


def test_list_accounts(mpt_ops):
    """Test listing accounts with a limit."""
    limit = 10

    result = mpt_ops.accounts.accounts.fetch_page(limit=limit)

    assert len(result) > 0


def test_create_account(created_account):
    result = created_account

    assert result is not None


def test_update_account(mpt_ops, created_account, account_factory, account_icon):
    """Test updating an account synchronously."""
    updated_data = account_factory(name="Updated Account Name")

    result = mpt_ops.accounts.accounts.update(created_account.id, updated_data, file=account_icon)

    assert result is not None


def test_update_account_invalid_data(mpt_ops, account_factory, created_account, account_icon):
    """Test updating an account with invalid data raises a 400 error."""
    updated_data = account_factory(name="")

    with pytest.raises(MPTAPIError, match=r"400 Bad Request"):
        mpt_ops.accounts.accounts.update(created_account.id, updated_data, file=account_icon)


def test_update_account_not_found(mpt_ops, account_factory, invalid_account_id, account_icon):
    """Test updating a non-existent account raises a 404 error."""
    non_existent_account = account_factory(name="Non Existent Account")

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.accounts.accounts.update(
            invalid_account_id, non_existent_account, file=account_icon
        )


def test_account_enable(mpt_ops, created_account):
    """Test enabling an account synchronously."""
    mpt_ops.accounts.accounts.disable(created_account.id)

    result = mpt_ops.accounts.accounts.enable(created_account.id)

    assert result is not None


def test_account_enable_not_found(mpt_ops, invalid_account_id):
    """Test enabling a non-existent account raises a 404 error."""
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.accounts.accounts.enable(invalid_account_id)


def test_account_disable(mpt_ops, created_account):
    result = mpt_ops.accounts.accounts.disable(created_account.id)

    assert result is not None


def test_account_disable_not_found(mpt_ops, invalid_account_id):
    """Test disabling a non-existent account raises a 404 error."""
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.accounts.accounts.disable(invalid_account_id)


def test_account_rql_filter(mpt_ops, account_id):
    """Test filtering accounts using RQL synchronously."""
    selected_fields = ["-address"]
    filtered_accounts = (
        mpt_ops.accounts.accounts.filter(RQLQuery(id=account_id))
        .filter(RQLQuery(name="Test Api Client Vendor"))
        .select(*selected_fields)
    )

    result = list(filtered_accounts.iterate())

    assert len(result) > 0
