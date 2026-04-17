import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def async_vendor_media_service(async_mpt_vendor, program_id):
    return async_mpt_vendor.program.programs.media(program_id)


@pytest.fixture
async def created_media_from_file(async_vendor_media_service, media_data_factory, logo_fd):
    media_data = media_data_factory()
    media = await async_vendor_media_service.create(media_data, file=logo_fd)
    yield media, media_data
    try:
        await async_vendor_media_service.delete(media.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete media {media.id}: {error.title}")  # noqa: WPS421


@pytest.fixture
async def created_media_from_url(
    async_vendor_media_service, media_data_factory, video_url, logo_fd
):
    media_data = media_data_factory(media_type="Video")

    media_data["url"] = video_url
    media = await async_vendor_media_service.create(media_data, file=logo_fd)
    yield media, media_data
    try:
        await async_vendor_media_service.delete(media.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete media {media.id}: {error.title}")  # noqa: WPS421


def test_create_media(created_media_from_file):  # noqa: AAA01
    result, media_data = created_media_from_file

    assert result.name == media_data["name"]
    assert result.description == media_data["description"]


def test_create_media_from_url(created_media_from_url):  # noqa: AAA01
    result, media_data = created_media_from_url

    assert result.name == media_data["name"]
    assert result.description == media_data["description"]


async def test_update_media(async_vendor_media_service, created_media_from_file):
    media, _ = created_media_from_file
    update_data = {"name": "E2E Updated Program Media"}

    result = await async_vendor_media_service.update(media.id, update_data)

    assert result.name == update_data["name"]


async def test_delete_media(async_vendor_media_service, created_media_from_file):
    media, _ = created_media_from_file

    result = await async_vendor_media_service.delete(media.id)

    assert result is None


async def test_get_media(async_vendor_media_service, media_id):
    result = await async_vendor_media_service.get(media_id)

    assert result.id == media_id


async def test_get_media_invalid_id(async_vendor_media_service, invalid_media_id):
    with pytest.raises(MPTAPIError):
        await async_vendor_media_service.get(invalid_media_id)


async def test_filter_and_select_media(async_vendor_media_service, media_id):
    select_fields = ["-revision", "-audit"]
    filtered_media = async_vendor_media_service.filter(RQLQuery(id=media_id)).select(*select_fields)

    result = [media async for media in filtered_media.iterate()]

    assert len(result) == 1


async def test_media_publish(async_vendor_media_service, created_media_from_file):
    media, _ = created_media_from_file

    result = await async_vendor_media_service.publish(media.id)

    assert result.status == "Published"


async def test_media_unpublish(async_vendor_media_service, created_media_from_file):
    media, _ = created_media_from_file
    await async_vendor_media_service.publish(media.id)

    result = await async_vendor_media_service.unpublish(media.id)

    assert result.status == "Unpublished"
