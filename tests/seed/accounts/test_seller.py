import pytest

from seed.accounts.seller import build_seller_data, create_seller, seed_seller
from seed.context import Context


@pytest.fixture
def context_without_data() -> Context:
    return Context()


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
    create_mock = mocker.AsyncMock(return_value={"id": "SEL-1111-1111"})
    operations_client.accounts.sellers.create = create_mock

    result = await create_seller(
        mpt_operations=operations_client,
    )

    assert result == {"id": "SEL-1111-1111"}
    args, _ = create_mock.await_args
    payload = args[0]
    assert payload["name"] == "E2E Seeded Seller"


async def test_seed_seller(mocker):
    mock_init_resource = mocker.patch(
        "seed.accounts.seller.init_resource", new_callable=mocker.AsyncMock
    )

    await seed_seller()

    mock_init_resource.assert_awaited_once()
