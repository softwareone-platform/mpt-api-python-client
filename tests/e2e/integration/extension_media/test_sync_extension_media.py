import pytest

from tests.e2e.helper import assert_service_filter_with_iterate

pytestmark = [
    pytest.mark.flaky,
]


def test_create_extension_media(created_media, media_data):
    result = created_media.name

    assert result == media_data["name"]


def test_filter_extension_media(extension_media_service, created_media):
    assert_service_filter_with_iterate(extension_media_service, created_media.id, None)  # act


def test_update_extension_media(extension_media_service, created_media, short_uuid):
    update_data = {"name": f"e2e updated {short_uuid}"}

    result = extension_media_service.update(created_media.id, update_data)

    assert result.name == update_data["name"]


def test_publish_extension_media(extension_media_service, created_media):
    result = extension_media_service.publish(created_media.id)

    assert result.status == "Published"


def test_unpublish_extension_media(extension_media_service, created_media):
    extension_media_service.publish(created_media.id)

    result = extension_media_service.unpublish(created_media.id)

    assert result.status == "Unpublished"


def test_delete_extension_media(extension_media_service, created_media):
    extension_media_service.delete(created_media.id)  # act
