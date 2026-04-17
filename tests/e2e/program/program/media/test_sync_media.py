import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def vendor_media_service(mpt_vendor, program_id):
    return mpt_vendor.program.programs.media(program_id)


@pytest.fixture
def created_media_from_file(vendor_media_service, media_data_factory, logo_fd):
    media_data = media_data_factory()
    media = vendor_media_service.create(media_data, file=logo_fd)
    yield media, media_data
    try:
        vendor_media_service.delete(media.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete media {media.id}: {error.title}")  # noqa: WPS421


@pytest.fixture
def created_media_from_url(vendor_media_service, media_data_factory, video_url, logo_fd):
    media_data = media_data_factory(media_type="Video")

    media_data["url"] = video_url
    media = vendor_media_service.create(media_data, file=logo_fd)
    yield media, media_data
    try:
        vendor_media_service.delete(media.id)
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


def test_update_media(vendor_media_service, created_media_from_file):
    media, _ = created_media_from_file
    update_data = {"name": "E2E Updated Program Media"}

    result = vendor_media_service.update(media.id, update_data)

    assert result.name == update_data["name"]


def test_delete_media(vendor_media_service, created_media_from_file):
    media, _ = created_media_from_file

    result = vendor_media_service.delete(media.id)

    assert result is None


def test_get_media(vendor_media_service, media_id):
    result = vendor_media_service.get(media_id)

    assert result.id == media_id


def test_get_media_invalid_id(vendor_media_service, invalid_media_id):
    with pytest.raises(MPTAPIError):
        vendor_media_service.get(invalid_media_id)


def test_filter_and_select_media(vendor_media_service, media_id):
    select_fields = ["-revision", "-audit"]
    filtered_media = vendor_media_service.filter(RQLQuery(id=media_id)).select(*select_fields)

    result = list(filtered_media.iterate())

    assert len(result) == 1


def test_media_publish(vendor_media_service, created_media_from_file):
    media, _ = created_media_from_file

    result = vendor_media_service.publish(media.id)

    assert result.status == "Published"


def test_media_unpublish(vendor_media_service, created_media_from_file):
    media, _ = created_media_from_file
    vendor_media_service.publish(media.id)

    result = vendor_media_service.unpublish(media.id)

    assert result.status == "Unpublished"
