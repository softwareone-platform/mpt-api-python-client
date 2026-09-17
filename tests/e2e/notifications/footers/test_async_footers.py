import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import (
    assert_async_service_filter_with_iterate,
    assert_async_update_resource,
)

pytestmark = [pytest.mark.flaky]


def test_create_footer(async_created_footer, footer_data):
    result = async_created_footer.content

    assert result == footer_data["content"]


async def test_get_footer(async_footers_service, async_created_footer):
    result = await async_footers_service.get(async_created_footer.id)

    assert result.id == async_created_footer.id


async def test_get_footer_not_found(async_footers_service):
    bogus_id = "FLV-0000-0000"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_footers_service.get(bogus_id)


async def test_update_footer(async_footers_service, async_created_footer, short_uuid):
    new_content = f"e2e footer updated {short_uuid}"

    await assert_async_update_resource(  # act
        async_footers_service, async_created_footer.id, "content", new_content
    )


async def test_delete_footer(async_footers_service, async_created_footer):
    await async_footers_service.delete(async_created_footer.id)

    result = await async_footers_service.get(async_created_footer.id)

    assert result.status == "Deleted"


async def test_delete_footer_not_found(async_footers_service):
    bogus_id = "FLV-0000-0000"

    with pytest.raises(MPTAPIError):
        await async_footers_service.delete(bogus_id)


async def test_filter_footers(async_footers_service, async_created_footer):
    await assert_async_service_filter_with_iterate(  # act
        async_footers_service, async_created_footer.id, None
    )
