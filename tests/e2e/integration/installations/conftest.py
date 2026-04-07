import pytest

from mpt_api_client.exceptions import MPTAPIError


@pytest.fixture
def installations_service(mpt_vendor):
    return mpt_vendor.integration.installations


@pytest.fixture
def async_installations_service(async_mpt_vendor):
    return async_mpt_vendor.integration.installations


@pytest.fixture
def installation_modules():
    return [
        {"id": "MOD-0478"},
        {"id": "MOD-1239"},
        {"id": "MOD-1756"},
        {"id": "MOD-4525"},
        {"id": "MOD-8352"},
        {"id": "MOD-8743"},
        {"id": "MOD-9042"},
    ]


@pytest.fixture
def installation_data(extension_id, installation_modules):
    return {
        "extension": {"id": extension_id},
        "modules": installation_modules,
    }


@pytest.fixture
def invite_data(extension_id):
    return {
        "extension": {"id": extension_id},
        "invitation": {
            "message": "E2E testing - Delete",
            "validity": "7d",
        },
    }


@pytest.fixture
def created_installation(installations_service, installation_data):
    installation = installations_service.create(installation_data)

    yield installation

    try:
        installations_service.delete(installation.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete installation {installation.id}: {error.title}")  # noqa: WPS421


@pytest.fixture
def created_installation_invite(installations_service, invite_data):
    invite = installations_service.create(invite_data)

    yield invite

    try:
        installations_service.delete(invite.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete installation {invite.id}: {error.title}")  # noqa: WPS421


@pytest.fixture
async def async_created_installation(async_installations_service, installation_data):
    installation = await async_installations_service.create(installation_data)

    yield installation

    try:
        await async_installations_service.delete(installation.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete installation {installation.id}: {error.title}")  # noqa: WPS421


@pytest.fixture
async def async_created_installation_invite(async_installations_service, invite_data):
    invite = await async_installations_service.create(invite_data)

    yield invite

    try:
        await async_installations_service.delete(invite.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete installation {invite.id}: {error.title}")  # noqa: WPS421
