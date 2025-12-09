import pytest

from seed.accounts.licensee import build_licensee_data, create_licensee, seed_licensee
from seed.context import Context


@pytest.fixture
def context_with_data() -> Context:
    ctx = Context()
    ctx["accounts.client_account.id"] = "ACC-1111-1111"
    ctx["accounts.seller.id"] = "SEL-2222-2222"
    ctx["accounts.buyer.id"] = "BUY-3333-3333"
    ctx["accounts.user_group.id"] = "UGR-4444-4444"
    return ctx


def test_build_licensee_data(context_with_data):
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
        "seller": {"id": "SEL-2222-2222"},
        "buyer": {"id": "BUY-3333-3333"},
        "account": {"id": "ACC-1111-1111"},
        "eligibility": {"client": True, "partner": False},
        "groups": [{"id": "UGR-4444-4444"}],
        "type": "Client",
        "status": "Enabled",
        "defaultLanguage": "en-US",
    }

    result = build_licensee_data(context=context_with_data)

    assert result == expected


async def test_create_licensee(mocker, client_client, context_with_data):  # noqa: WPS218
    create_mock = mocker.AsyncMock(return_value={"id": "licensee-1"})
    client_client.accounts.licensees.create = create_mock

    result = await create_licensee(
        context=context_with_data,
        mpt_client=client_client,
    )

    assert result == {"id": "licensee-1"}
    args, _ = create_mock.await_args
    payload = args[0]
    assert payload["name"] == "E2E Seeded Licensee"
    assert payload["account"]["id"] == "ACC-1111-1111"
    assert payload["seller"]["id"] == "SEL-2222-2222"
    assert payload["buyer"]["id"] == "BUY-3333-3333"
    assert payload["groups"][0]["id"] == "UGR-4444-4444"


async def test_seed_licensee(mocker):
    mock_init_resource = mocker.patch(
        "seed.accounts.licensee.init_resource", new_callable=mocker.AsyncMock
    )

    await seed_licensee()

    mock_init_resource.assert_awaited_once()
