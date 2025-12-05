import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import (
    assert_async_service_filter_with_iterate,
    assert_async_update_resource,
    async_create_fixture_resource_and_delete,
)

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def async_listings_service(async_mpt_ops):
    return async_mpt_ops.catalog.listings


@pytest.fixture
async def async_created_listing(async_listings_service, listing_data):
    async with async_create_fixture_resource_and_delete(
        async_listings_service, listing_data
    ) as listing:
        yield listing


def test_create_listing(async_created_listing, product_id):
    result = async_created_listing.product.id

    assert result == product_id


async def test_get_listing(async_listings_service, listing_id):
    result = await async_listings_service.get(listing_id)

    assert result.id == listing_id


async def test_filter_listings(async_listings_service, listing_id):
    await assert_async_service_filter_with_iterate(async_listings_service, listing_id, None)  # act


async def test_get_listing_not_found(async_listings_service):
    bogus_id = "LST-0000-NOTFOUND"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_listings_service.get(bogus_id)


async def test_update_listing(async_listings_service, async_created_listing, short_uuid):
    await assert_async_update_resource(
        async_listings_service, async_created_listing.id, "notes", f"delete-me {short_uuid}"
    )  # act


async def test_delete_listing(async_listings_service, async_created_listing):
    await async_listings_service.delete(async_created_listing.id)  # act
