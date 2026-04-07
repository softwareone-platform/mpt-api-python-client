from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.chat_messages import ChatMessage

pytestmark = [pytest.mark.flaky, pytest.mark.skip(reason="Unskip when MPT-19696 unblocked")]


async def test_list_channel_messages(async_channel_messages_service):
    result = await async_channel_messages_service.fetch_page(limit=1)

    assert len(result) > 0
    assert all(isinstance(message, ChatMessage) for message in result)


async def test_list_channel_messages_not_found(async_mpt_ops, invalid_channel_id):
    with pytest.raises(MPTAPIError) as error:
        await async_mpt_ops.helpdesk.channels.messages(invalid_channel_id).fetch_page(limit=1)
    assert error.value.status_code == HTTPStatus.NOT_FOUND
