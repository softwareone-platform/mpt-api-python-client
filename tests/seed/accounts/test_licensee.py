import pytest

from mpt_api_client.models.model import Model
from mpt_api_client.resources.accounts.licensees import Licensee
from seed.accounts.licensee import build_licensee_data, create_licensee, seed_licensee
from seed.context import Context


@pytest.fixture
def licensee():
    return Licensee({
        "id": "LIC-123",
        "name": "E2E Seeded Licensee",
        "account": {"id": "ACC-1086-6867"},
        "contact": {
            "firstName": "first",
            "lastName": "last",
            "email": "created.licensee@example.com",
        },
        "address": {
            "addressLine1": "123 Main St",
            "city": "Los Angeles",
            "state": "CA",
            "postCode": "67890",
            "country": "US",
        },
        "group": {"id": "UG-123"},
    })


def test_build_licensee_data(context: Context, monkeypatch):
    monkeypatch.setenv("CLIENT_ACCOUNT_ID", "ACC-1086-6867")
    context["accounts.user_group.id"] = "UG-123"
    context.set_resource("accounts.user_group", Model({"id": "UG-123"}))
    context["accounts.seller.id"] = "SEL-123"
    context["accounts.buyer.id"] = "BUY-123"
    context["accounts.account.id"] = "ACC-1086-6867"
    expected = {
        "name": "E2E Seeded Licensee",
        "address": {
            "addressLine1": "123 Main St",
            "city": "Los Angeles",
            "state": "CA",
            "postCode": "67890",
            "country": "US",
        },
        "useBuyerAddress": False,
        "seller": {"id": "SEL-123"},
        "buyer": {"id": "BUY-123"},
        "account": {"id": "ACC-1086-6867"},
        "eligibility": {"client": True, "partner": False},
        "groups": [{"id": "UG-123"}],
        "type": "Client",
        "status": "Enabled",
        "defaultLanguage": "en-US",
    }

    result = build_licensee_data(context=context)

    assert result == expected


async def test_create_licensee(mocker, operations_client, licensee):
    create_mock = mocker.AsyncMock(return_value=licensee)
    operations_client.accounts.licensees.create = create_mock
    mocker.patch("seed.accounts.licensee.build_licensee_data")

    result = await create_licensee(operations_client)

    assert result == licensee
    create_mock.assert_awaited_once()


async def test_seed_licensee(mocker):
    init_resource = mocker.patch("seed.accounts.licensee.init_resource", autospec=True)

    await seed_licensee()  # act

    init_resource.assert_awaited_once()
