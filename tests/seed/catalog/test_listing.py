import pytest

from seed.catalog.listing import create_listing, seed_listing
from seed.context import Context


@pytest.fixture
def context_with_data() -> Context:
    """
    Create a Context pre-populated with product, seller, authorization, account, and price list IDs for tests.
    
    Returns:
        Context: A Context containing the following keys set to test IDs:
            - "catalog.product.id": "prod-123"
            - "accounts.seller.id": "seller-456"
            - "catalog.authorization.id": "auth-789"
            - "accounts.account.id": "acct-321"
            - "catalog.price_list.id": "pl-654"
    """
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


async def test_seed_listing_skips(mocker, context_with_data):
    context_with_data["catalog.listing.id"] = "lst-existing"
    create_mock = mocker.patch("seed.catalog.listing.create_listing", new_callable=mocker.AsyncMock)

    await seed_listing(context_with_data)

    create_mock.assert_not_called()


async def test_seed_listing_creates(mocker, context_with_data):
    create_mock = mocker.patch(
        "seed.catalog.listing.create_listing",
        new_callable=mocker.AsyncMock,
        return_value=mocker.Mock(id="lst-999"),
    )

    await seed_listing(context_with_data)

    create_mock.assert_awaited_once()
    assert context_with_data.get_string("catalog.listing.id") == "lst-999"