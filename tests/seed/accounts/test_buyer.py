import io
from unittest.mock import AsyncMock, patch

import pytest
from seed.accounts.buyer import build_buyer_data, get_buyer, init_buyer, seed_buyer
from mpt_api_client.resources.accounts.buyers import Buyer, AsyncBuyersService
from seed.context import Context


@pytest.fixture
def buyer():
    return Buyer({"id": "BUY-123", "name": "Test Buyer"})


@pytest.fixture
def buyers_service():
    return AsyncMock(spec=AsyncBuyersService)


async def test_get_buyer(
    context: Context, operations_client, buyer, buyers_service
) -> None:
    context["accounts.buyer.id"] = buyer.id
    buyers_service.get.return_value = buyer
    operations_client.accounts.buyers = buyers_service

    result = await get_buyer(context=context, mpt_operations=operations_client)

    assert result == buyer
    assert context.get_resource("accounts.buyer", buyer.id) == buyer


async def test_get_buyer_without_id(context: Context) -> None:
    result = await get_buyer(context=context)
    assert result is None


def test_build_buyer_data(context: Context) -> None:
    context["accounts.account.id"] = "ACC-456"
    expected_data = {
        "name": "E2E Seeded Buyer",
        "account": {
            "id": "ACC-456",
        },
        "contact": {
            "firstName": "first",
            "lastName": "last",
            "email": "created.buyer@example.com",
        },
        "address": {
            "addressLine1": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "postCode": "12345",
            "country": "US",
        },
    }

    result = build_buyer_data(context=context)

    assert result == expected_data


async def test_init_buyer(
    context: Context, operations_client, buyers_service, buyer
) -> None:
    buyers_service.create.return_value = buyer
    operations_client.accounts.buyers = buyers_service

    result = await init_buyer(context, mpt_operations=operations_client)

    assert result == buyer
    buyers_service.create.assert_called_once()


async def test_init_buyer_create_new(
    context: Context, operations_client, buyers_service, buyer
) -> None:
    buyers_service.create.return_value = buyer
    operations_client.accounts.buyers = buyers_service

    with (
        patch("seed.accounts.buyer.get_buyer", return_value=None),
        patch("seed.accounts.buyer.icon", new=AsyncMock()),
        patch("pathlib.Path.open", return_value=AsyncMock()),
    ):
        result = await init_buyer(context, mpt_operations=operations_client)

        assert result == buyer
        buyers_service.create.assert_called_once()


async def test_seed_buyer() -> None:
    with (
        patch("seed.accounts.buyer.init_buyer", new_callable=AsyncMock) as mock_init_buyer,
    ):
        await seed_buyer()  # act
        mock_init_buyer.assert_awaited_once()
