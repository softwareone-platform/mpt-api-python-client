import pytest

from tests.e2e.helper import (
    async_create_fixture_resource_and_delete,
    create_fixture_resource_and_delete,
)


@pytest.fixture
def chat_answers_service(mpt_ops, created_chat):
    return mpt_ops.helpdesk.chats.answers(created_chat.id)


@pytest.fixture
def async_chat_answers_service(async_mpt_ops, created_chat):
    return async_mpt_ops.helpdesk.chats.answers(created_chat.id)


@pytest.fixture
def chat_answer_data(short_uuid, created_published_form):
    return {
        "name": f"e2e answer {short_uuid}",
        "form": created_published_form.to_dict(),
    }


@pytest.fixture
def async_chat_answer_data(short_uuid, async_created_published_form):
    return {
        "name": f"e2e answer {short_uuid}",
        "form": async_created_published_form.to_dict(),
    }


@pytest.fixture
def created_chat_answer(chat_answers_service, chat_answer_data):
    with create_fixture_resource_and_delete(chat_answers_service, chat_answer_data) as chat_answer:
        yield chat_answer


@pytest.fixture
def submitted_chat_answer(chat_answers_service, created_chat_answer):
    return chat_answers_service.submit(created_chat_answer.id)


@pytest.fixture
async def async_created_chat_answer(async_chat_answers_service, async_chat_answer_data):
    async with async_create_fixture_resource_and_delete(
        async_chat_answers_service, async_chat_answer_data
    ) as chat_answer:
        yield chat_answer


@pytest.fixture
async def async_submitted_chat_answer(async_chat_answers_service, async_created_chat_answer):
    return await async_chat_answers_service.submit(async_created_chat_answer.id)


@pytest.fixture(scope="session")
def invalid_chat_answer_id():
    return "ANS-0000-0000"
