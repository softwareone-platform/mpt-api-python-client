import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def async_media_service(async_mpt_vendor, product_id):
    return async_mpt_vendor.catalog.products.media(product_id)


@pytest.fixture
def async_vendor_media_service(async_mpt_vendor, product_id):
    return async_mpt_vendor.catalog.products.media(product_id)


@pytest.fixture
async def created_media_from_file_async(logger, async_media_service, media_data, test_media_file):
    media = await async_media_service.create(media_data, test_media_file)
    yield media
    try:
        await async_media_service.delete(media.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete media {media.id}: {error.title}")


@pytest.fixture
async def created_media_from_url_async(logger, async_media_service, media_data, jpg_url):
    media_data["url"] = jpg_url
    media = await async_media_service.create(media_data)
    yield media
    try:
        await async_media_service.delete(media.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete media {media.id}: {error.title}")


def test_create_media_async(created_media_from_file_async, media_data):  # noqa: AAA01
    assert created_media_from_file_async.name == media_data["name"]
    assert created_media_from_file_async.description == media_data["description"]


def test_create_media_async_from_url(created_media_from_file_async, media_data):  # noqa: AAA01
    assert created_media_from_file_async.name == media_data["name"]
    assert created_media_from_file_async.description == media_data["description"]


async def test_update_media_async(async_media_service, created_media_from_file_async):
    update_data = {"name": "Updated e2e test media - please delete"}

    result = await async_media_service.update(created_media_from_file_async.id, update_data)

    assert result.name == update_data["name"]


async def test_media_lifecycle_async(
    async_mpt_vendor, async_mpt_ops, created_media_from_file_async
):
    await async_mpt_vendor.catalog.products.media(created_media_from_file_async.product.id).review(
        created_media_from_file_async.id
    )
    await async_mpt_ops.catalog.products.media(created_media_from_file_async.product.id).publish(
        created_media_from_file_async.id
    )
    await async_mpt_vendor.catalog.products.media(
        created_media_from_file_async.product.id
    ).unpublish(created_media_from_file_async.id)


async def test_delete_media_async(async_vendor_media_service, created_media_from_file_async):
    await async_vendor_media_service.delete(created_media_from_file_async.id)  # act

    with pytest.raises(MPTAPIError):
        await async_vendor_media_service.get(created_media_from_file_async.id)


async def test_get_media_async(async_vendor_media_service, created_media_from_file_async):
    result = await async_vendor_media_service.get(created_media_from_file_async.id)

    assert result.id == created_media_from_file_async.id


async def test_download_media_async(async_vendor_media_service, created_media_from_file_async):
    result = await async_vendor_media_service.download(created_media_from_file_async.id)

    assert result.file_contents is not None
    assert result.filename == "logo.png"


async def test_get_not_found_media_async(async_vendor_media_service):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_vendor_media_service.get("INVALID-ID")
