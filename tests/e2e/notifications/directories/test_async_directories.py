import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import assert_async_service_filter_with_iterate

pytestmark = [pytest.mark.flaky]


async def test_get_directory(async_directories_service, directory_id):
    result = await async_directories_service.get(directory_id)

    assert result.id == directory_id


async def test_get_directory_not_found(async_directories_service):
    bogus_id = "DIR-0000-0000"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_directories_service.get(bogus_id)


async def test_filter_directories(async_directories_service, directory_id):
    await assert_async_service_filter_with_iterate(
        async_directories_service, directory_id, None
    )  # act
