import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.models import FileModel
from tests.e2e.helper import assert_async_service_filter_with_iterate

pytestmark = [pytest.mark.flaky]


@pytest.mark.skip(reason="unable to create extensions for testing")
def test_create_extension(async_created_extension, extension_data):
    result = async_created_extension.name

    assert result == extension_data["name"]


async def test_get_extension(async_extensions_service, extension_id):
    result = await async_extensions_service.get(extension_id)

    assert result.id == extension_id


async def test_get_extension_not_found(async_extensions_service):
    bogus_id = "EXT-0000-0000"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_extensions_service.get(bogus_id)


@pytest.mark.skip(reason="unable to create extensions for testing")
async def test_update_extension(
    async_extensions_service, async_created_extension, logo_fd, short_uuid
):
    update_data = {"name": f"e2e - please delete {short_uuid}"}

    result = await async_extensions_service.update(
        async_created_extension.id, update_data, file=logo_fd
    )

    assert result.name == update_data["name"]


@pytest.mark.skip(reason="unable to create extensions for testing")
async def test_delete_extension(async_extensions_service, async_created_extension):
    await async_extensions_service.delete(async_created_extension.id)  # act


async def test_filter_extensions(async_extensions_service, extension_id):
    await assert_async_service_filter_with_iterate(
        async_extensions_service, extension_id, None
    )  # act


@pytest.mark.skip(reason="unable to create extensions for testing")
async def test_download_icon(async_extensions_service, async_created_extension):
    result = await async_extensions_service.download_icon(async_created_extension.id)

    assert isinstance(result, FileModel)


@pytest.mark.skip(reason="unable to create extensions for testing")
async def test_publish_extension(async_extensions_service, async_created_extension):
    result = await async_extensions_service.publish(async_created_extension.id)

    assert result.status == "Public"


@pytest.mark.skip(reason="unable to create extensions for testing")
async def test_unpublish_extension(async_extensions_service, async_created_extension):
    await async_extensions_service.publish(async_created_extension.id)

    result = await async_extensions_service.unpublish(async_created_extension.id)

    assert result.status == "Private"
