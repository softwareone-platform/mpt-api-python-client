from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.chat_participants import ChatParticipant

pytestmark = [pytest.mark.flaky]


def test_list_chat_participants(chat_participants_service):
    result = chat_participants_service.fetch_page(limit=1)

    assert len(result) > 0
    assert all(isinstance(participant, ChatParticipant) for participant in result)


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")  # noqa: AAA01
def test_create_chat_participant(created_chat_participant):
    assert isinstance(created_chat_participant, ChatParticipant)


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_update_chat_participant(chat_participants_service, created_chat_participant):
    result = chat_participants_service.update(created_chat_participant.id, {"status": "Active"})

    assert isinstance(result, ChatParticipant)


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_delete_chat_participant(chat_participants_service, created_chat_participant):
    result = created_chat_participant

    chat_participants_service.delete(result.id)


def test_update_chat_participant_not_found(chat_participants_service, invalid_chat_participant_id):
    with pytest.raises(MPTAPIError) as error:
        chat_participants_service.update(invalid_chat_participant_id, {"status": "Active"})

    assert error.value.status_code == HTTPStatus.NOT_FOUND


def test_delete_chat_participant_not_found(chat_participants_service, invalid_chat_participant_id):
    with pytest.raises(MPTAPIError) as error:
        chat_participants_service.delete(invalid_chat_participant_id)

    assert error.value.status_code == HTTPStatus.BAD_REQUEST  # TODO: verify 400 is OK instead 404
