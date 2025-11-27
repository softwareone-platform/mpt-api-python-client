import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def vendor_media_service(mpt_vendor, product_id):
    return mpt_vendor.catalog.products.media(product_id)


@pytest.fixture
def created_media_from_file(vendor_media_service, media_data, test_media_file):
    media = vendor_media_service.create(media_data, test_media_file)
    yield media
    try:
        vendor_media_service.delete(media.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete media {media.id}: {error.title}")


@pytest.fixture
def created_media_from_url(vendor_media_service, media_data, jpg_url):
    media_data["url"] = jpg_url
    media = vendor_media_service.create(media_data)
    yield media
    try:
        vendor_media_service.delete(media.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete media {media.id}: {error.title}")


def test_create_media(created_media_from_file, media_data):  # noqa: AAA01
    assert created_media_from_file.name == media_data["name"]
    assert created_media_from_file.description == media_data["description"]


def test_create_media_from_url(created_media_from_file, media_data):  # noqa: AAA01
    assert created_media_from_file.name == media_data["name"]
    assert created_media_from_file.description == media_data["description"]


def test_update_media(vendor_media_service, created_media_from_file):
    update_data = {"name": "Updated e2e test media - please delete"}

    result = vendor_media_service.update(created_media_from_file.id, update_data)

    assert result.name == update_data["name"]


def test_media_lifecycle(mpt_vendor, mpt_ops, created_media_from_file):  # noqa: AAA01
    mpt_vendor.catalog.products.media(created_media_from_file.product.id).review(
        created_media_from_file.id
    )
    mpt_ops.catalog.products.media(created_media_from_file.product.id).publish(
        created_media_from_file.id
    )
    mpt_vendor.catalog.products.media(created_media_from_file.product.id).unpublish(
        created_media_from_file.id
    )


def test_delete_media(vendor_media_service, created_media_from_file):
    vendor_media_service.delete(created_media_from_file.id)

    with pytest.raises(MPTAPIError):
        vendor_media_service.get(created_media_from_file.id)


def test_get_media(vendor_media_service, created_media_from_file):
    result = vendor_media_service.get(created_media_from_file.id)

    assert result.id == created_media_from_file.id


def test_download_media(vendor_media_service, created_media_from_file):
    result = vendor_media_service.download(created_media_from_file.id)

    assert result.file_contents is not None
    assert result.filename == "logo.png"


async def test_get_not_found_media(vendor_media_service):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await vendor_media_service.get("INVALID-ID")
