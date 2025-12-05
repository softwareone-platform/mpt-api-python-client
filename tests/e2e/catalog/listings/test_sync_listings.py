import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import (
    assert_service_filter_with_iterate,
    assert_update_resource,
    create_fixture_resource_and_delete,
)

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def listings_service(mpt_ops):
    return mpt_ops.catalog.listings


@pytest.fixture
def created_listing(listings_service, listing_data):
    with create_fixture_resource_and_delete(listings_service, listing_data) as listing:
        yield listing


def test_create_listing(created_listing, product_id):
    result = created_listing.product.id

    assert result == product_id


def test_get_listing_by_id(listings_service, listing_id):
    result = listings_service.get(listing_id)

    assert result.id == listing_id


def test_filter_listings(listings_service, listing_id):
    assert_service_filter_with_iterate(
        listings_service,
        listing_id,
        None,
    )  # act


def test_get_listing_not_found(listings_service):
    bogus_id = "LST-0000-NOTFOUND"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        listings_service.get(bogus_id)


def test_update_listing(listings_service, created_listing, short_uuid):
    assert_update_resource(
        listings_service, created_listing.id, "notes", f"delete-me {short_uuid}"
    )  # act


def test_delete_listing(listings_service, created_listing):
    listings_service.delete(created_listing.id)  # act
