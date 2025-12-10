import pytest

from mpt_api_client.resources.accounts.buyers import Buyer
from seed.accounts.buyer import build_buyer_data, create_buyer, seed_buyer
from seed.context import Context


@pytest.fixture
def buyer():
    return Buyer({"id": "BUY-123", "name": "Test Buyer"})


def test_build_buyer_data(context: Context):
    context["accounts.account.id"] = "ACC-1086-6867"
    context["accounts.seller.id"] = "SEL-9999-9999"
    expected_data = {
        "name": "E2E Seeded Buyer",
        "account": {
            "id": "ACC-1086-6867",
        },
        "contact": {
            "firstName": "first",
            "lastName": "last",
            "email": "created.buyer@example.com",
        },
        "address": {
            "addressLine1": "123 Main St",
            "city": "Los Angeles",
            "state": "CA",
            "postCode": "12345",
            "country": "US",
        },
        "sellers": [{"id": "SEL-9999-9999"}],
    }

    result = build_buyer_data(context=context)

    assert result == expected_data


async def test_create_buyer(mocker, context: Context, operations_client, buyer):
    context["accounts.seller.id"] = "SEL-9999-9999"
    context["accounts.account.id"] = "ACC-1086-6867"
    operations_client.accounts.buyers.create = mocker.AsyncMock(return_value=buyer)

    result = await create_buyer(context, operations_client)

    assert result == buyer


async def test_seed_buyer(mocker):
    init_resource = mocker.patch("seed.accounts.buyer.init_resource", autospec=True)

    await seed_buyer()  # act

    init_resource.assert_awaited_once()
