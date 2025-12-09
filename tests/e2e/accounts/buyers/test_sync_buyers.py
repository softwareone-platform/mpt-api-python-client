import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_buyer(mpt_ops, buyer_factory, client_account_id, account_icon):
    """Fixture to create and yield a buyer for testing."""
    new_buyer_request_data = buyer_factory(
        name="E2E Created Buyer",
        account_id=client_account_id,
    )

    new_buyer = mpt_ops.accounts.buyers.create(new_buyer_request_data, file=account_icon)

    yield new_buyer

    try:
        mpt_ops.accounts.buyers.delete(new_buyer.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete buyer: {error.title}")  # noqa: WPS421


def test_get_buyer_by_id(mpt_ops, buyer_id):
    result = mpt_ops.accounts.buyers.get(buyer_id)

    assert result is not None


def test_list_buyers(mpt_ops):
    """Test listing buyers with a limit."""
    limit = 10

    result = mpt_ops.accounts.buyers.fetch_page(limit=limit)

    assert len(result) > 0


def test_get_buyer_by_id_not_found(mpt_ops, invalid_buyer_id):
    """Test fetching a buyer by an invalid ID raises a 404 error."""
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.accounts.buyers.get(invalid_buyer_id)


def test_filter_buyers(mpt_ops, buyer_id):
    """Test filtering buyers using RQL synchronously."""
    select_fields = ["-address"]
    filtered_buyers = (
        mpt_ops.accounts.buyers.filter(RQLQuery(id=buyer_id))
        .filter(RQLQuery(name="E2E Seeded Buyer"))
        .select(*select_fields)
    )

    result = list(filtered_buyers.iterate())

    assert len(result) == 1


def test_create_buyer(created_buyer):
    result = created_buyer

    assert result is not None


def test_delete_buyer(mpt_ops, created_buyer):
    mpt_ops.accounts.buyers.delete(created_buyer.id)  # act


def test_delete_buyer_not_found(mpt_ops, invalid_buyer_id):
    """Test deleting a non-existent buyer raises a 404 error."""
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.accounts.buyers.delete(invalid_buyer_id)


def test_update_buyer(mpt_ops, buyer_factory, client_account_id, account_icon, created_buyer):
    """Test updating a buyer synchronously."""
    updated_buyer_data = buyer_factory(name="E2E Updated Buyer", account_id=client_account_id)

    result = mpt_ops.accounts.buyers.update(created_buyer.id, updated_buyer_data, file=account_icon)

    assert result is not None


def test_update_buyer_not_found(
    mpt_ops, buyer_factory, client_account_id, account_icon, invalid_buyer_id
):
    """Test updating a non-existent buyer raises a 404 error."""
    updated_buyer_data = buyer_factory(name="Nonexistent Buyer", account_id=client_account_id)

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.accounts.buyers.update(invalid_buyer_id, updated_buyer_data, file=account_icon)


def test_buyer_disable(mpt_ops, created_buyer):
    result = mpt_ops.accounts.buyers.disable(created_buyer.id)

    assert result is not None


def test_buyer_disable_not_found(mpt_ops, invalid_buyer_id):
    """Test disabling a non-existent buyer raises a 404 error."""
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.accounts.buyers.disable(invalid_buyer_id)


def test_buyer_enable(mpt_ops, created_buyer):
    """Test enabling a buyer synchronously."""
    mpt_ops.accounts.buyers.disable(created_buyer.id)

    result = mpt_ops.accounts.buyers.enable(created_buyer.id)

    assert result is not None


def test_buyer_enable_not_found(mpt_ops, invalid_buyer_id):
    """Test enabling a non-existent buyer raises a 404 error."""
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.accounts.buyers.enable(invalid_buyer_id)
