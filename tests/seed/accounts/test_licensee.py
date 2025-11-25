from unittest.mock import AsyncMock, patch

import pytest

from mpt_api_client.resources.accounts.licensees import AsyncLicenseesService, Licensee
from seed.accounts.licensee import build_licensee_data, get_licensee, init_licensee, seed_licensee
from seed.context import Context


@pytest.fixture
def licensee():
    return Licensee({"id": "LIC-123", "name": "Test Licensee"})


@pytest.fixture
def licensees_service():
    return AsyncMock(spec=AsyncLicenseesService)


async def test_get_licensee(
    context: Context, client_client, licensee, licensees_service
) -> None:
    context["accounts.licensee.id"] = licensee.id
    licensees_service.get.return_value = licensee
    client_client.accounts.licensees = licensees_service

    result = await get_licensee(context=context, mpt_operations=client_client)

    assert result == licensee
    assert context.get_resource("accounts.licensee", licensee.id) == licensee


async def test_get_licensee_without_id(context: Context) -> None:
    licensee = await get_licensee(context=context)
    assert licensee is None


def test_build_licensee_data(context: Context) -> None:
    context["accounts.account.id"] = "ACC-123"
    licensee_data = {
        "name": "E2E Seeded Licensee",
        "account": {"id": "ACC-123"},
        "contact": {
            "firstName": "first",
            "lastName": "last",
            "email": "created.licensee@example.com",
        },
        "address": {
            "addressLine1": "456 Licensee St",
            "city": "Los Angeles",
            "state": "CA",
            "postCode": "67890",
            "country": "US",
        },
    }

    result = build_licensee_data(context=context)

    assert result == licensee_data


async def test_init_licensee(
    context: Context, client_client, licensees_service, licensee
) -> None:
    licensees_service.create.return_value = licensee
    client_client.accounts.licensees = licensees_service

    result = await init_licensee(context, mpt_operations=client_client)

    assert result == licensee
    licensees_service.create.assert_called_once()


async def test_init_licensee_create_new(
    context: Context, client_client, licensees_service, licensee
) -> None:
    licensees_service.create.return_value = licensee
    client_client.accounts.licensees = licensees_service

    with (
        patch("seed.accounts.licensee.get_licensee", return_value=None),
        patch("seed.accounts.licensee.icon", new=AsyncMock()),
        patch("pathlib.Path.open", return_value=AsyncMock()),
    ):
        result = await init_licensee(context, mpt_operations=client_client)

        assert result == licensee
        licensees_service.create.assert_called_once()


async def test_seed_licensee() -> None:
    with (
        patch("seed.accounts.licensee.init_licensee", new_callable=AsyncMock) as mock_init_licensee,
    ):
        await seed_licensee()  # act
        mock_init_licensee.assert_awaited_once()
