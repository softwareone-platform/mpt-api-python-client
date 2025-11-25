from unittest.mock import AsyncMock, patch

import pytest

from mpt_api_client.resources.accounts.sellers import AsyncSellersService, Seller
from seed.accounts.seller import build_seller_data, get_seller, init_seller, seed_seller
from seed.context import Context


@pytest.fixture
def seller():
    return Seller({"id": "SEL-123", "name": "Test Seller"})


@pytest.fixture
def sellers_service():
    return AsyncMock(spec=AsyncSellersService)


async def test_get_seller(
    context: Context, operations_client, seller, sellers_service
) -> None:
    context["accounts.seller.id"] = seller.id
    sellers_service.get.return_value = seller
    operations_client.accounts.sellers = sellers_service

    result = await get_seller(context=context, mpt_operations=operations_client)

    assert result == seller
    assert context.get_resource("accounts.seller", seller.id) == seller


async def test_get_seller_without_id(context: Context) -> None:
    result = await get_seller(context=context)
    assert result is None


def test_build_seller_data():
    external_id = "test-external-id"
    seller_data = {
        "name": "E2E Seeded Seller",
        "address": {
            "addressLine1": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "postCode": "12345",
            "country": "US",
        },
        "currencies": ["USD", "EUR"],
        "externalId": external_id,  # Must be unique in Marketplace
    }

    result = build_seller_data(external_id=external_id)

    assert result == seller_data


async def test_init_seller(
    context: Context, operations_client, sellers_service, seller
) -> None:
    sellers_service.create.return_value = seller
    operations_client.accounts.sellers = sellers_service

    result = await init_seller(context, mpt_operations=operations_client)
    assert result == seller
    sellers_service.create.assert_called_once()


async def test_init_seller_create_new(
    context: Context, operations_client, sellers_service, seller
) -> None:
    sellers_service.create.return_value = seller
    operations_client.accounts.sellers = sellers_service
    with patch("seed.accounts.seller.get_seller", return_value=None):
        result = await init_seller(context, mpt_operations=operations_client)

        assert result == seller
        sellers_service.create.assert_called_once()


async def test_seed_seller() -> None:
    with (
        patch("seed.accounts.seller.init_seller", new_callable=AsyncMock) as mock_init_seller,
    ):
        await seed_seller()  # act
        mock_init_seller.assert_awaited_once()
