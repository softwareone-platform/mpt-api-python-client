import pytest

from tests.e2e.helper import (
    async_create_fixture_resource_and_delete,
    create_fixture_resource_and_delete,
)


@pytest.fixture
def chat_messages_service(mpt_ops, created_chat):
    return mpt_ops.helpdesk.chats.messages(created_chat.id)


@pytest.fixture
def async_chat_messages_service(async_mpt_ops, created_chat):
    return async_mpt_ops.helpdesk.chats.messages(created_chat.id)


@pytest.fixture
def chat_message_data(short_uuid):
    return {
        "content": f"e2e message - {short_uuid}",
    }


@pytest.fixture
def created_chat_message(chat_messages_service, chat_message_data):
    with create_fixture_resource_and_delete(
        chat_messages_service, chat_message_data
    ) as chat_message:
        yield chat_message


@pytest.fixture
async def async_created_chat_message(async_chat_messages_service, chat_message_data):
    async with async_create_fixture_resource_and_delete(
        async_chat_messages_service, chat_message_data
    ) as chat_message:
        yield chat_message


@pytest.fixture(scope="session")
def invalid_chat_message_id():
    return "MSG-0000-0000-0000"
