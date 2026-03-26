from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.chat_links import ChatLink

pytestmark = [pytest.mark.flaky]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_list_chat_links(async_chat_links_service):
    result = await async_chat_links_service.fetch_page(limit=1)

    assert len(result) > 0
    assert all(isinstance(link, ChatLink) for link in result)


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")  # noqa: AAA01
def test_create_chat_link(async_created_chat_link, chat_link_data):
    assert async_created_chat_link.id is not None
    assert async_created_chat_link.to_dict().get("uri") == chat_link_data["uri"]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_update_chat_link_name(async_chat_links_service, async_created_chat_link, short_uuid):
    new_name = f"e2e updated link - {short_uuid}"

    result = await async_chat_links_service.update(
        async_created_chat_link.id,
        {"name": new_name},
    )

    assert result.id == async_created_chat_link.id
    assert result.to_dict().get("name") == new_name


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_delete_chat_link(async_chat_links_service, async_created_chat_link):
    result = async_created_chat_link

    await async_chat_links_service.delete(result.id)


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_update_chat_link_not_found(async_chat_links_service, invalid_chat_link_id):
    with pytest.raises(MPTAPIError) as error:
        await async_chat_links_service.update(
            invalid_chat_link_id,
            {"name": "updated name"},
        )
    assert error.value.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_delete_chat_link_not_found(async_chat_links_service, invalid_chat_link_id):
    with pytest.raises(MPTAPIError) as error:
        await async_chat_links_service.delete(invalid_chat_link_id)
    assert error.value.status_code == HTTPStatus.NOT_FOUND
