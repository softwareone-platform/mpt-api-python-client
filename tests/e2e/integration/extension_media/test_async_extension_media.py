import pytest

from tests.e2e.helper import assert_async_service_filter_with_iterate

pytestmark = [
    pytest.mark.flaky,
]


def test_create_extension_media_async(async_created_media, media_data):
    result = async_created_media.name

    assert result == media_data["name"]


async def test_filter_extension_media_async(async_extension_media_service, async_created_media):
    await assert_async_service_filter_with_iterate(
        async_extension_media_service, async_created_media.id, None
    )  # act


async def test_update_extension_media_async(
    async_extension_media_service, async_created_media, short_uuid
):
    update_data = {"name": f"e2e updated {short_uuid}"}

    result = await async_extension_media_service.update(async_created_media.id, update_data)

    assert result.name == update_data["name"]


async def test_publish_extension_media_async(async_extension_media_service, async_created_media):
    result = await async_extension_media_service.publish(async_created_media.id)

    assert result.status == "Published"


async def test_download_extension_media_async(async_extension_media_service, async_created_media):
    result = await async_extension_media_service.download(async_created_media.id)

    assert result.file_contents is not None


async def test_unpublish_extension_media_async(async_extension_media_service, async_created_media):
    await async_extension_media_service.publish(async_created_media.id)

    result = await async_extension_media_service.unpublish(async_created_media.id)

    assert result.status == "Unpublished"


async def test_delete_extension_media_async(async_extension_media_service, async_created_media):
    await async_extension_media_service.delete(async_created_media.id)  # act
