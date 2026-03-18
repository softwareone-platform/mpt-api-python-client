import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


async def test_list_chat_links(async_chat_links_service):
    result = await async_chat_links_service.fetch_page(limit=1)

    assert len(result) > 0


def test_create_chat_link(async_created_chat_link, chat_link_data):  # noqa: AAA01
    assert async_created_chat_link.id is not None
    assert async_created_chat_link.to_dict().get("uri") == chat_link_data["uri"]


async def test_update_chat_link_name(async_chat_links_service, async_created_chat_link, short_uuid):
    new_name = f"e2e updated link - {short_uuid}"

    result = await async_chat_links_service.update(
        async_created_chat_link.id,
        {"name": new_name},
    )

    assert result.id == async_created_chat_link.id
    assert result.to_dict().get("name") == new_name


async def test_delete_chat_link(async_chat_links_service, async_created_chat_link):
    result = async_created_chat_link

    await async_chat_links_service.delete(result.id)


async def test_update_chat_link_not_found(async_chat_links_service, invalid_chat_link_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_chat_links_service.update(
            invalid_chat_link_id,
            {"name": "updated name"},
        )


async def test_delete_chat_link_not_found(async_chat_links_service, invalid_chat_link_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_chat_links_service.delete(invalid_chat_link_id)
