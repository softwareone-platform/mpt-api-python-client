import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_list_chat_participants(chat_participants_service):
    result = chat_participants_service.fetch_page(limit=1)

    assert len(result) > 0


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")  # noqa: AAA01
def test_create_chat_participant(created_chat_participant):
    assert created_chat_participant.id is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_update_chat_participant(chat_participants_service, created_chat_participant):
    result = chat_participants_service.update(created_chat_participant.id, {"status": "Active"})

    assert result.id == created_chat_participant.id


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_delete_chat_participant(chat_participants_service, created_chat_participant):
    result = created_chat_participant

    chat_participants_service.delete(result.id)


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_update_chat_participant_not_found(chat_participants_service, invalid_chat_participant_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        chat_participants_service.update(invalid_chat_participant_id, {"status": "Active"})


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_delete_chat_participant_not_found(chat_participants_service, invalid_chat_participant_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        chat_participants_service.delete(invalid_chat_participant_id)
