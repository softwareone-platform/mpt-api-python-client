from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.chat_attachments import ChatAttachment

pytestmark = [pytest.mark.flaky]


async def test_list_chat_attachments(async_chat_attachments_service, async_created_chat_attachment):
    result = await async_chat_attachments_service.fetch_page(limit=1)

    assert len(result) > 0
    assert all(isinstance(attachment, ChatAttachment) for attachment in result)


def test_create_chat_attachment(async_created_chat_attachment, chat_attachment_data):  # noqa: AAA01
    assert async_created_chat_attachment.id is not None
    assert async_created_chat_attachment.to_dict().get("name") == chat_attachment_data["name"]


async def test_get_chat_attachment(async_chat_attachments_service, async_created_chat_attachment):
    result = await async_chat_attachments_service.get(async_created_chat_attachment.id)

    assert result.id == async_created_chat_attachment.id


async def test_update_chat_attachment(
    async_chat_attachments_service, async_created_chat_attachment, short_uuid
):
    updated_name = f"e2e updated attachment - {short_uuid}"

    result = await async_chat_attachments_service.update(
        async_created_chat_attachment.id,
        {"name": updated_name, "description": updated_name},
    )

    assert result.id == async_created_chat_attachment.id
    assert result.to_dict().get("name") == updated_name


async def test_download_chat_attachment(
    async_chat_attachments_service, async_created_chat_attachment
):
    result = await async_chat_attachments_service.download(
        async_created_chat_attachment.id,
        accept="application/pdf",
    )

    assert result.file_contents is not None


async def test_delete_chat_attachment(async_chat_attachments_service, chat_attachment_data, pdf_fd):
    created = await async_chat_attachments_service.create(chat_attachment_data, file=pdf_fd)

    result = await async_chat_attachments_service.delete(created.id)

    assert result is None


async def test_get_chat_attachment_not_found(
    async_chat_attachments_service, invalid_chat_attachment_id
):
    with pytest.raises(MPTAPIError) as error:
        await async_chat_attachments_service.get(invalid_chat_attachment_id)
    assert error.value.status_code == HTTPStatus.NOT_FOUND


async def test_update_chat_attachment_not_found(
    async_chat_attachments_service, invalid_chat_attachment_id
):
    with pytest.raises(MPTAPIError) as error:
        await async_chat_attachments_service.update(
            invalid_chat_attachment_id,
            {"description": "updated description"},
        )
    assert error.value.status_code == HTTPStatus.NOT_FOUND


async def test_delete_chat_attachment_not_found(
    async_chat_attachments_service, invalid_chat_attachment_id
):
    with pytest.raises(MPTAPIError) as error:
        await async_chat_attachments_service.delete(invalid_chat_attachment_id)
    assert error.value.status_code == HTTPStatus.NOT_FOUND
