import pytest

from mpt_api_client.exceptions import MPTAPIError


@pytest.fixture(scope="session")
def extension_id(e2e_config):
    return e2e_config["integration.extension.id"]


@pytest.fixture
def extension_media_service(mpt_vendor, extension_id):
    return mpt_vendor.integration.extensions.media(extension_id)


@pytest.fixture
def async_extension_media_service(async_mpt_vendor, extension_id):
    return async_mpt_vendor.integration.extensions.media(extension_id)


@pytest.fixture
def media_data(short_uuid):
    return {
        "name": f"e2e - please delete {short_uuid}",
        "description": "Created by automated E2E tests. Safe to delete.",
        "mediaType": "Image",
        "url": "https://example.com/image.png",
        "displayOrder": 1,
    }


@pytest.fixture
def created_media(extension_media_service, media_data, logo_fd):
    media = extension_media_service.create(media_data, file=logo_fd)

    yield media

    try:
        extension_media_service.delete(media.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete media {media.id}: {error.title}")  # noqa: WPS421


@pytest.fixture
async def async_created_media(async_extension_media_service, media_data, logo_fd):
    media = await async_extension_media_service.create(media_data, file=logo_fd)

    yield media

    try:
        await async_extension_media_service.delete(media.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete media {media.id}: {error.title}")  # noqa: WPS421
