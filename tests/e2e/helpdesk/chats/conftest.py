import pytest


@pytest.fixture(scope="session")
def chat_id(e2e_config):
    return e2e_config["helpdesk.chat.id"]


@pytest.fixture(scope="session")
def invalid_chat_id():
    return "CHT-0000-0000-0000"
