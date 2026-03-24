import pytest


@pytest.fixture
def chat_answer_parameters_service(mpt_ops, chat_id, created_chat_answer):
    return mpt_ops.helpdesk.chats.answers(chat_id).parameters(created_chat_answer.id)


@pytest.fixture
def async_chat_answer_parameters_service(async_mpt_ops, chat_id, async_created_chat_answer):
    return async_mpt_ops.helpdesk.chats.answers(chat_id).parameters(async_created_chat_answer.id)


@pytest.fixture
def invalid_chat_answer_parameter_id():
    return "PAR-0000-0000"
