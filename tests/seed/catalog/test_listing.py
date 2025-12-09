import pytest

from seed.catalog.listing import create_listing, seed_listing
from seed.context import Context


@pytest.fixture
def context_with_data() -> Context:
    ctx = Context()
    ctx["catalog.product.id"] = "prod-123"
    ctx["accounts.seller.id"] = "seller-456"
    ctx["catalog.authorization.id"] = "auth-789"
    ctx["accounts.account.id"] = "acct-321"
    ctx["catalog.price_list.id"] = "pl-654"
    return ctx


async def test_create_listing(mocker, operations_client, context_with_data):  # noqa: WPS218
    create_mock = mocker.AsyncMock(return_value={"id": "lst-1"})
    operations_client.catalog.listings.create = create_mock

    result = await create_listing(operations_client, context_with_data)

    assert result == {"id": "lst-1"}
    args, _ = create_mock.await_args
    payload = args[0]
    assert payload["product"]["id"] == "prod-123"
    assert payload["seller"]["id"] == "seller-456"
    assert payload["authorization"]["id"] == "auth-789"
    assert payload["vendor"]["id"] == "acct-321"
    assert payload["priceList"]["id"] == "pl-654"


async def test_seed_listing(mocker, context_with_data):
    init_resource = mocker.patch(
        "seed.catalog.listing.init_resource",
        new_callable=mocker.AsyncMock,
        return_value=mocker.Mock(id="lst-999"),
    )

    await seed_listing()

    init_resource.assert_awaited_once_with("catalog.listing.id", create_listing)
