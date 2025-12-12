import pytest

from mpt_api_client.resources.accounts.sellers import Seller
from seed.accounts.seller import (
    build_seller_data,
    create_seller,
    seed_seller,
)


@pytest.fixture
def seller():
    return Seller({"id": "SEL-123", "name": "Test Seller"})


def test_build_seller_data():
    external_id = "test-external-id"
    seller_data = {
        "name": "E2E Seeded Seller",
        "address": {
            "addressLine1": "123 Main St",
            "city": "Los Angeles",
            "state": "CA",
            "postCode": "12345",
            "country": "US",
        },
        "currencies": ["USD", "EUR"],
        "externalId": external_id,  # Must be unique in Marketplace
    }

    result = build_seller_data(external_id=external_id)

    assert result == seller_data


async def test_create_seller(mocker, operations_client):
    seller = Seller({"id": "SEL-123"})
    create_mock = mocker.AsyncMock(return_value=seller)
    operations_client.accounts.sellers.create = create_mock

    result = await create_seller(operations_client)

    assert result == seller
    create_mock.assert_called_once()


async def test_seed_seller(mocker):
    init_resource = mocker.patch("seed.accounts.seller.init_resource", autospec=True)

    await seed_seller()  # act

    init_resource.assert_awaited_once()
