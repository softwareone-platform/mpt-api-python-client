import pytest

from seed.accounts.buyer import build_buyer_data, create_buyer, seed_buyer
from seed.context import Context


@pytest.fixture
def context_with_data() -> Context:
    ctx = Context()
    ctx["accounts.client_account.id"] = "ACC-1111-1111"
    ctx["accounts.seller.id"] = "SEL-2222-2222"
    return ctx


def test_build_buyer_data(context_with_data):
    expected_data = {
        "name": "E2E Seeded Buyer",
        "account": {
            "id": "ACC-1111-1111",
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
        "sellers": [{"id": "SEL-2222-2222"}],
    }

    result = build_buyer_data(context=context_with_data)

    assert result == expected_data


async def test_create_buyer(mocker, operations_client, context_with_data):
    create_mock = mocker.AsyncMock(return_value={"id": "buyer-1"})
    operations_client.accounts.buyers.create = create_mock

    result = await create_buyer(
        context=context_with_data,
        mpt_operations=operations_client,
    )

    assert result == {"id": "buyer-1"}
    args, _ = create_mock.await_args
    payload = args[0]
    assert payload["name"] == "E2E Seeded Buyer"
    assert payload["account"]["id"] == "ACC-1111-1111"
    assert payload["sellers"][0]["id"] == "SEL-2222-2222"


async def test_seed_buyer(mocker):
    mock_init_resource = mocker.patch(
        "seed.accounts.buyer.init_resource", new_callable=mocker.AsyncMock
    )

    await seed_buyer()

    mock_init_resource.assert_awaited_once()
