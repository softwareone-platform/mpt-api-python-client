import pytest


@pytest.fixture
def chat_id(e2e_config):
    return e2e_config["helpdesk.chat.id"]


@pytest.fixture
def invalid_chat_id():
    return "CHT-0000-0000-0000"
