from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.chat_participants import ChatParticipant

pytestmark = [pytest.mark.flaky]


async def test_list_chat_participants(async_chat_participants_service):
    result = await async_chat_participants_service.fetch_page(limit=1)

    assert len(result) > 0
    assert all(isinstance(participant, ChatParticipant) for participant in result)


@pytest.mark.skip(reason="Unskip after MPT-20015 completed")  # noqa: AAA01
def test_create_chat_participant(async_created_chat_participant):
    assert isinstance(async_created_chat_participant, ChatParticipant)


@pytest.mark.skip(reason="Unskip after MPT-20015 completed")
async def test_update_chat_participant(
    async_chat_participants_service, async_created_chat_participant
):
    result = await async_chat_participants_service.update(
        async_created_chat_participant.id,
        {"status": "Active"},
    )

    assert isinstance(result, ChatParticipant)


@pytest.mark.skip(reason="Unskip after MPT-20015 completed")
async def test_delete_chat_participant(
    async_chat_participants_service, async_created_chat_participant
):
    result = async_created_chat_participant

    await async_chat_participants_service.delete(result.id)


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
