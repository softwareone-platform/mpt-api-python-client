from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.models import ModelCollection
from mpt_api_client.resources.helpdesk.chat_participants import ChatParticipant

pytestmark = [pytest.mark.flaky]


async def test_list_chat_participants(async_chat_participants_service):
    result = await async_chat_participants_service.fetch_page(limit=1)

    assert len(result) > 0
    assert all(isinstance(participant, ChatParticipant) for participant in result)


def test_create_chat_participant(async_created_chat_participant, contact_id):  # noqa: AAA01
    assert isinstance(async_created_chat_participant, ModelCollection)
    assert all(isinstance(cp, ChatParticipant) for cp in async_created_chat_participant)
    chat_participants_list = async_created_chat_participant.to_list()
    assert any(cp["contact"]["id"] == contact_id for cp in chat_participants_list)


async def test_update_chat_participant(
    async_chat_participants_service, async_created_chat_participant
):
    chat_participant = async_created_chat_participant[0].to_dict()
    new_muted_status = not chat_participant["muted"]
    chat_participant["muted"] = new_muted_status

    result = await async_chat_participants_service.update(chat_participant["id"], chat_participant)

    assert result.to_dict().get("muted") == new_muted_status


async def test_delete_chat_participant(
    async_chat_participants_service, async_created_chat_participant, contact_id
):
    result = next(
        chat_participant
        for chat_participant in async_created_chat_participant.to_list()
        if chat_participant["contact"]["id"] == contact_id
    )

    await async_chat_participants_service.delete(result["id"])


async def test_update_chat_participant_not_found(
    async_chat_participants_service, invalid_chat_participant_id
):
    with pytest.raises(MPTAPIError) as error:
        await async_chat_participants_service.update(
            invalid_chat_participant_id,
            {"status": "Active"},
        )
    assert error.value.status_code == HTTPStatus.NOT_FOUND


async def test_delete_chat_participant_not_found(
    async_chat_participants_service, invalid_chat_participant_id
):
    with pytest.raises(MPTAPIError) as error:
        await async_chat_participants_service.delete(invalid_chat_participant_id)
    assert error.value.status_code == HTTPStatus.BAD_REQUEST  # TODO: verify 400 is OK instead 404
