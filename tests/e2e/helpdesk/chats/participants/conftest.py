import pytest

from tests.e2e.helper import (
    async_create_fixture_resource_and_delete,
    create_fixture_resource_and_delete,
)


@pytest.fixture
def chat_participants_service(mpt_ops, chat_id):
    return mpt_ops.helpdesk.chats.participants(chat_id)


@pytest.fixture
def async_chat_participants_service(async_mpt_ops, chat_id):
    return async_mpt_ops.helpdesk.chats.participants(chat_id)


@pytest.fixture
def chat_participant_data(account_id, user_id):
    return {
        "identity": {"id": user_id},
        "account": {"id": account_id},
    }


@pytest.fixture
def created_chat_participant(chat_participants_service, chat_participant_data):
    with create_fixture_resource_and_delete(
        chat_participants_service, chat_participant_data
    ) as chat_participant:
        yield chat_participant


@pytest.fixture
async def async_created_chat_participant(async_chat_participants_service, chat_participant_data):
    async with async_create_fixture_resource_and_delete(
        async_chat_participants_service, chat_participant_data
    ) as chat_participant:
        yield chat_participant


@pytest.fixture
def invalid_chat_participant_id():
    return "CHP-0000-0000-0000"
