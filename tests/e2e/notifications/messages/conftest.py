import pytest


@pytest.fixture
def message_data(short_uuid, account_id):
    return {
        "title": "e2e - please delete",
        "content": "This is an e2e test message - please delete",
        "category": "general",
        "priority": "normal",
        "account": {
            "id": account_id,
        },
        "externalIds": {"test": f"e2e-delete-{short_uuid}"},
    }


@pytest.fixture
def message_id(e2e_config):
    return e2e_config.get("notifications.message.id")


@pytest.fixture
def invalid_message_id(e2e_config):
    return "MSG-000-000-000-000"
