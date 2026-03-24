import pytest

from tests.e2e.helper import (
    async_create_fixture_resource_and_delete,
    create_fixture_resource_and_delete,
)


@pytest.fixture
def chat_answers_service(mpt_ops, chat_id):
    return mpt_ops.helpdesk.chats.answers(chat_id)


@pytest.fixture
def async_chat_answers_service(async_mpt_ops, chat_id):
    return async_mpt_ops.helpdesk.chats.answers(chat_id)


@pytest.fixture
def chat_answer_data(short_uuid):
    return {
        "name": f"e2e answer {short_uuid}",
    }


@pytest.fixture
def created_chat_answer(chat_answers_service, chat_answer_data):
    with create_fixture_resource_and_delete(chat_answers_service, chat_answer_data) as chat_answer:
        yield chat_answer


@pytest.fixture
async def async_created_chat_answer(async_chat_answers_service, chat_answer_data):
    async with async_create_fixture_resource_and_delete(
        async_chat_answers_service, chat_answer_data
    ) as chat_answer:
        yield chat_answer


@pytest.fixture
def invalid_chat_answer_id():
    return "ANS-0000-0000"
