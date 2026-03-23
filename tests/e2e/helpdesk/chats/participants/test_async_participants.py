import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_list_chat_participants(async_chat_participants_service):
    result = await async_chat_participants_service.fetch_page(limit=1)

    assert len(result) > 0


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")  # noqa: AAA01
def test_create_chat_participant(async_created_chat_participant):
    assert async_created_chat_participant.id is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_update_chat_participant(
    async_chat_participants_service, async_created_chat_participant
):
    result = await async_chat_participants_service.update(
        async_created_chat_participant.id,
        {"status": "Active"},
    )

    assert result.id == async_created_chat_participant.id


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_delete_chat_participant(
    async_chat_participants_service, async_created_chat_participant
):
    result = async_created_chat_participant

    await async_chat_participants_service.delete(result.id)


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_update_chat_participant_not_found(
    async_chat_participants_service, invalid_chat_participant_id
):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_chat_participants_service.update(
            invalid_chat_participant_id,
            {"status": "Active"},
        )


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_delete_chat_participant_not_found(
    async_chat_participants_service, invalid_chat_participant_id
):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_chat_participants_service.delete(invalid_chat_participant_id)
