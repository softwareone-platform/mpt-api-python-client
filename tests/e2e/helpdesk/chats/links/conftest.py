import pytest

from tests.e2e.helper import (
    async_create_fixture_resource_and_delete,
    create_fixture_resource_and_delete,
)


@pytest.fixture
def chat_links_service(mpt_ops, chat_id):
    return mpt_ops.helpdesk.chats.links(chat_id)


@pytest.fixture
def async_chat_links_service(async_mpt_ops, chat_id):
    return async_mpt_ops.helpdesk.chats.links(chat_id)


@pytest.fixture
def chat_link_data(short_uuid):
    return {
        "uri": f"https://example.com/e2e-link-{short_uuid}",
        "name": f"e2e link - {short_uuid}",
    }


@pytest.fixture
def created_chat_link(chat_links_service, chat_link_data):
    with create_fixture_resource_and_delete(chat_links_service, chat_link_data) as chat_link:
        yield chat_link


@pytest.fixture
async def async_created_chat_link(async_chat_links_service, chat_link_data):
    async with async_create_fixture_resource_and_delete(
        async_chat_links_service, chat_link_data
    ) as chat_link:
        yield chat_link


@pytest.fixture
def invalid_chat_link_id():
    return "LNK-0000-0000-0000"
