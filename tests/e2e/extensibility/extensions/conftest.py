import pytest

from mpt_api_client.exceptions import MPTAPIError


@pytest.fixture
def extensions_service(mpt_vendor):
    return mpt_vendor.extensibility.extensions


@pytest.fixture
def async_extensions_service(async_mpt_vendor):
    return async_mpt_vendor.extensibility.extensions


@pytest.fixture(scope="session")
def extension_id(e2e_config):
    return e2e_config["extensibility.extension.id"]


@pytest.fixture
def extension_data(short_uuid):
    return {
        "name": f"e2e - please delete {short_uuid}",
        "shortDescription": f"E2E test extension {short_uuid}",
        "longDescription": "Created by automated E2E tests. Safe to delete.",
        "website": "https://example.com",
    }


@pytest.fixture
def created_extension(extensions_service, extension_data, logo_fd):
    extension = extensions_service.create(extension_data, file=logo_fd)

    yield extension

    try:
        extensions_service.delete(extension.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete extension {extension.id}: {error.title}")  # noqa: WPS421


@pytest.fixture
async def async_created_extension(async_extensions_service, extension_data, logo_fd):
    extension = await async_extensions_service.create(extension_data, file=logo_fd)

    yield extension

    try:
        await async_extensions_service.delete(extension.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete extension {extension.id}: {error.title}")  # noqa: WPS421
