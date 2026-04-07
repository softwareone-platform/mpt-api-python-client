import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.models import FileModel
from tests.e2e.helper import assert_service_filter_with_iterate

pytestmark = [
    pytest.mark.flaky,
]


def test_create_extension(created_extension, extension_data):
    result = created_extension.name

    assert result == extension_data["name"]


def test_get_extension(extensions_service, extension_id):
    result = extensions_service.get(extension_id)

    assert result.id == extension_id


def test_get_extension_not_found(extensions_service):
    bogus_id = "EXT-0000-0000"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        extensions_service.get(bogus_id)


def test_update_extension(extensions_service, created_extension, logo_fd, short_uuid):
    update_data = {"name": f"e2e - please delete {short_uuid}"}

    result = extensions_service.update(created_extension.id, update_data, file=logo_fd)

    assert result.name == update_data["name"]


def test_delete_extension(extensions_service, created_extension):
    extensions_service.delete(created_extension.id)  # act


def test_filter_extensions(extensions_service, extension_id):
    assert_service_filter_with_iterate(extensions_service, extension_id, None)  # act


@pytest.mark.skip(reason="unable to create extensions for testing")
def test_download_icon(extensions_service, created_extension):
    result = extensions_service.download_icon(created_extension.id)

    assert isinstance(result, FileModel)


@pytest.mark.skip(reason="unable to create extensions for testing")
def test_publish_extension(extensions_service, created_extension):
    result = extensions_service.publish(created_extension.id)

    assert result.status == "Public"


@pytest.mark.skip(reason="unable to create extensions for testing")
def test_unpublish_extension(extensions_service, created_extension):
    extensions_service.publish(created_extension.id)

    result = extensions_service.unpublish(created_extension.id)

    assert result.status == "Private"
