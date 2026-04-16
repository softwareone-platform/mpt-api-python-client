import pytest


@pytest.fixture
def chat_participants_service(mpt_ops, created_chat):
    return mpt_ops.helpdesk.chats.participants(created_chat.id)


@pytest.fixture
def async_chat_participants_service(async_mpt_ops, created_chat):
    return async_mpt_ops.helpdesk.chats.participants(created_chat.id)


@pytest.fixture
def contact_id(e2e_config):
    return e2e_config["notifications.contact.id"]


@pytest.fixture
def chat_participant_data(contact_id):
    return {"contact": {"id": contact_id}}


@pytest.fixture
def created_chat_participant(chat_participants_service, chat_participant_data):
    return chat_participants_service.create([chat_participant_data])


@pytest.fixture
async def async_created_chat_participant(async_chat_participants_service, chat_participant_data):
    return await async_chat_participants_service.create([chat_participant_data])


@pytest.fixture(scope="session")
def invalid_chat_participant_id():
    return "CHP-0000-0000-0000"
