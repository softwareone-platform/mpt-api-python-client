import pytest

from mpt_api_client.resources.accounts.buyers import AsyncBuyersService, Buyer
from seed.accounts.buyer import build_buyer_data, get_buyer, init_buyer, seed_buyer
from seed.context import Context


@pytest.fixture
def buyer():
    return Buyer({"id": "BUY-123", "name": "Test Buyer"})


@pytest.fixture
def buyers_service(mocker):
    return mocker.Mock(spec=AsyncBuyersService)


async def test_get_buyer(context: Context, operations_client, buyer, buyers_service):
    context["accounts.buyer.id"] = buyer.id
    buyers_service.get.return_value = buyer
    operations_client.accounts.buyers = buyers_service

    result = await get_buyer(context=context, mpt_operations=operations_client)

    assert result == buyer
    assert context.get_resource("accounts.buyer", buyer.id) == buyer


async def test_get_buyer_without_id(context: Context):
    result = await get_buyer(context=context)
    assert result is None


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


async def test_init_buyer(context: Context, operations_client, buyers_service, buyer, mocker):
    buyers_service.create.return_value = buyer
    operations_client.accounts.buyers = buyers_service
    mock_get_buyer = mocker.patch("seed.accounts.buyer.get_buyer", new_callable=mocker.AsyncMock)
    mock_get_buyer.return_value = buyer
    result = await init_buyer(context=context, mpt_operations=operations_client)
    assert result == buyer
    buyers_service.create.assert_not_called()


async def test_init_buyer_create_new(  # noqa: WPS211
    context: Context,
    operations_client,
    buyers_service,
    buyer,
    monkeypatch,
    fs,
):
    buyers_service.create.return_value = buyer
    operations_client.accounts.buyers = buyers_service
    monkeypatch.setenv("CLIENT_ACCOUNT_ID", "ACC-1086-6867")
    context["accounts.seller.id"] = "SEL-9999-9999"
    fs.create_file("/fake/path/buyer.txt", contents=b"fake_buyer_bytes")
    fs.create_file("/mpt_api_client/seed/data/logo.png", contents=b"fake_icon_bytes")
    result = await init_buyer(context=context, mpt_operations=operations_client)
    assert result == buyer
    buyers_service.create.assert_called_once()


async def test_seed_buyer(mocker):
    mock_init_buyer = mocker.patch("seed.accounts.buyer.init_buyer", new_callable=mocker.AsyncMock)
    await seed_buyer()  # act
    mock_init_buyer.assert_awaited_once()
