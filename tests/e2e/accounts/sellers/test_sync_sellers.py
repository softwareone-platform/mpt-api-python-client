import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_seller(mpt_ops, seller_factory, logger):
    ret_seller = None

    def _created_seller(
        external_id: str,
        name: str = "E2E Test Seller",
    ):
        nonlocal ret_seller  # noqa: WPS420
        seller_data = seller_factory(external_id=external_id, name=name)
        ret_seller = mpt_ops.accounts.sellers.create(seller_data)
        return ret_seller

    yield _created_seller

    if ret_seller:
        try:
            mpt_ops.accounts.sellers.delete(ret_seller.id)
        except MPTAPIError:
            print(f"TEARDOWN - Unable to delete seller {ret_seller.id}")  # noqa: WPS421


def test_get_seller_by_id(mpt_ops, seller_id):
    seller = mpt_ops.accounts.sellers.get(seller_id)
    assert seller is not None


def test_list_sellers(mpt_ops):
    limit = 10

    sellers = mpt_ops.accounts.sellers.fetch_page(limit=limit)

    assert len(sellers) > 0


def test_get_seller_by_id_not_found(mpt_ops, invalid_seller_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.accounts.sellers.get(invalid_seller_id)


def test_filter_sellers(mpt_ops, seller_id):
    select_fields = ["-address"]

    filtered_sellers = (
        mpt_ops.accounts.sellers.filter(RQLQuery(id=seller_id))
        .filter(RQLQuery(name="E2E Seeded Seller"))
        .select(*select_fields)
    )

    sellers = list(filtered_sellers.iterate())

    assert len(sellers) == 1


def test_create_seller(created_seller, timestamp):
    seller_data = created_seller(external_id=f"Create E2E Seller - {timestamp}")
    assert seller_data is not None


def test_delete_seller(mpt_ops, created_seller, timestamp):
    seller_data = created_seller(external_id=f"Delete E2E Seller - {timestamp}")
    mpt_ops.accounts.sellers.delete(seller_data.id)


def test_delete_seller_not_found(mpt_ops, invalid_seller_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.accounts.sellers.delete(invalid_seller_id)


def test_update_seller(mpt_ops, seller_factory, created_seller, timestamp):
    seller_data = created_seller(external_id=f"Update E2E Seller - {timestamp}")
    update_data = seller_factory(
        external_id=f"Update E2E Seller - {timestamp}",
        name=f"Updated Update E2E Seller - {timestamp}",
    )
    updated_seller = mpt_ops.accounts.sellers.update(seller_data.id, update_data)
    assert updated_seller is not None


def test_update_seller_mpt_error(mpt_ops, seller_factory, timestamp, invalid_seller_id):
    update_data = seller_factory(
        external_id=f"Async Update E2E Seller Not Found - {timestamp}",
        name=f"Updated Update E2E Seller Not Found - {timestamp}",
    )
    with pytest.raises(MPTAPIError):
        mpt_ops.accounts.sellers.update(invalid_seller_id, update_data)


def test_activate_seller(mpt_ops, created_seller, timestamp):
    seller_data = created_seller(external_id=f"Activate E2E Seller - {timestamp}")
    mpt_ops.accounts.sellers.disable(seller_data.id)
    activated_seller = mpt_ops.accounts.sellers.activate(seller_data.id)

    assert activated_seller is not None


def test_activate_seller_mpt_error(mpt_ops, invalid_seller_id):
    with pytest.raises(MPTAPIError):
        mpt_ops.accounts.sellers.activate(invalid_seller_id)


def test_deactivate_seller(mpt_ops, created_seller, timestamp):
    seller_data = created_seller(external_id=f"Deactivate E2E Seller - {timestamp}")
    deactivated_seller = mpt_ops.accounts.sellers.disable(seller_data.id)

    assert deactivated_seller is not None


def test_deactivate_seller_mpt_error(mpt_ops, invalid_seller_id):
    with pytest.raises(MPTAPIError):
        mpt_ops.accounts.sellers.disable(invalid_seller_id)


def test_disable_seller(mpt_ops, created_seller, timestamp):
    seller_data = created_seller(external_id=f"Disable E2E Seller - {timestamp}")
    disabled_seller = mpt_ops.accounts.sellers.disable(seller_data.id)

    assert disabled_seller is not None


def test_disable_seller_mpt_error(mpt_ops, invalid_seller_id):
    with pytest.raises(MPTAPIError):
        mpt_ops.accounts.sellers.disable(invalid_seller_id)
