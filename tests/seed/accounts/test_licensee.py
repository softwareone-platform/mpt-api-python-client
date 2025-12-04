import pytest

from mpt_api_client.models.model import Model
from mpt_api_client.resources.accounts.licensees import AsyncLicenseesService, Licensee
from seed.accounts.licensee import build_licensee_data, get_licensee, init_licensee, seed_licensee
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


@pytest.fixture
def licensees_service(mocker):
    return mocker.Mock(spec=AsyncLicenseesService)


async def test_get_licensee(context: Context, client_client, licensee, licensees_service):
    context["accounts.licensee.id"] = licensee.id
    licensees_service.get.return_value = licensee
    client_client.accounts.licensees = licensees_service

    result = await get_licensee(context=context, mpt_client=client_client)

    assert result == licensee
    assert context.get_resource("accounts.licensee", licensee.id) == licensee


async def test_get_licensee_without_id(context: Context):
    licensee = await get_licensee(context=context)
    assert licensee is None


def test_build_licensee_data(context: Context, monkeypatch):
    monkeypatch.setenv("CLIENT_ACCOUNT_ID", "ACC-1086-6867")
    context["accounts.user_group.id"] = "UG-123"
    context.set_resource("accounts.user_group", Model({"id": "UG-123"}))
    context["accounts.seller.id"] = "SEL-123"
    context["accounts.buyer.id"] = "BUY-123"
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


async def test_init_licensee(  # noqa: WPS211
    context: Context, client_client, licensees_service, licensee, monkeypatch, mocker, fs
):
    licensees_service.create.return_value = licensee
    client_client.accounts.licensees = licensees_service
    monkeypatch.setenv("CLIENT_ACCOUNT_ID", "ACC-1086-6867")
    context["accounts.user_group.id"] = "UG-123"
    context.set_resource("accounts.user_group", Model({"id": "UG-123"}))
    context["accounts.seller.id"] = "SEL-123"
    context["accounts.buyer.id"] = "BUY-123"
    mock_get_licensee = mocker.patch(
        "seed.accounts.licensee.get_licensee", new_callable=mocker.AsyncMock
    )
    mocker.patch(
        "seed.accounts.licensee.build_licensee_data", return_value=build_licensee_data(context)
    )
    mock_get_licensee.return_value = None
    fs.create_file("/mpt_api_client/seed/data/logo.png", contents=b"fake_icon_bytes")
    result = await init_licensee(context=context, mpt_client=client_client)
    assert result == licensee
    licensees_service.create.assert_called_once()


async def test_init_licensee_create_new(  # noqa: WPS211
    context: Context, client_client, licensees_service, licensee, monkeypatch, fs, mocker
):
    licensees_service.create.return_value = licensee
    client_client.accounts.licensees = licensees_service
    monkeypatch.setenv("CLIENT_ACCOUNT_ID", "ACC-1086-6867")
    context["accounts.user_group.id"] = "UG-123"
    context.set_resource("accounts.user_group", Model({"id": "UG-123"}))
    context["accounts.seller.id"] = "SEL-123"
    context["accounts.buyer.id"] = "BUY-123"
    fs.create_file("/mpt_api_client/seed/data/logo.png", contents=b"fake_icon_bytes")
    result = await init_licensee(context=context, mpt_client=client_client)
    assert result == licensee
    licensees_service.create.assert_called_once()


async def test_seed_licensee(mocker):
    mock_init_licensee = mocker.patch(
        "seed.accounts.licensee.init_licensee", new_callable=mocker.AsyncMock
    )
    await seed_licensee()  # act
    mock_init_licensee.assert_awaited_once()
