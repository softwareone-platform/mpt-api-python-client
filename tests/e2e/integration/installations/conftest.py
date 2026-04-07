import pytest

from mpt_api_client.exceptions import MPTAPIError


@pytest.fixture
def installations_service(mpt_ops):
    return mpt_ops.integration.installations


@pytest.fixture
def async_installations_service(async_mpt_ops):
    return async_mpt_ops.integration.installations


@pytest.fixture(scope="session")
def installation_id(e2e_config):
    return e2e_config["integration.installation.id"]


@pytest.fixture
def installation_data():
    return {
        "extension": {"id": "EXT-0000-0000"},
        "account": {"id": "ACC-0000-0000"},
        "modules": [],
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
async def async_created_installation(async_installations_service, installation_data):
    installation = await async_installations_service.create(installation_data)

    yield installation

    try:
        await async_installations_service.delete(installation.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete installation {installation.id}: {error.title}")  # noqa: WPS421
