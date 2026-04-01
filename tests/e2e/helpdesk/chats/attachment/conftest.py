import pytest

from mpt_api_client.exceptions import MPTAPIError


@pytest.fixture
def chat_attachments_service(mpt_ops, created_chat):
    return mpt_ops.helpdesk.chats.attachments(created_chat.id)


@pytest.fixture
def async_chat_attachments_service(async_mpt_ops, created_chat):
    return async_mpt_ops.helpdesk.chats.attachments(created_chat.id)


@pytest.fixture
def chat_attachment_data(short_uuid):
    attachment_name = f"e2e attachment - {short_uuid}"
    return {
        "name": attachment_name,
        "description": attachment_name,
    }


@pytest.fixture
def created_chat_attachment(chat_attachments_service, chat_attachment_data, pdf_fd):
    chat_attachment = chat_attachments_service.create(chat_attachment_data, file=pdf_fd)
    yield chat_attachment
    try:
        chat_attachments_service.delete(chat_attachment.id)
    except MPTAPIError as error:
        print(  # noqa: WPS421
            f"TEARDOWN - Unable to delete chat attachment {chat_attachment.id}: {error.title}"
        )


@pytest.fixture
async def async_created_chat_attachment(
    async_chat_attachments_service, chat_attachment_data, pdf_fd
):
    chat_attachment = await async_chat_attachments_service.create(chat_attachment_data, file=pdf_fd)
    yield chat_attachment
    try:
        await async_chat_attachments_service.delete(chat_attachment.id)
    except MPTAPIError as error:
        print(  # noqa: WPS421
            f"TEARDOWN - Unable to delete chat attachment {chat_attachment.id}: {error.title}"
        )


@pytest.fixture(scope="session")
def invalid_chat_attachment_id():
    return "ATT-0000-0000-0000-0000"
