import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_list_chat_attachments(async_chat_attachments_service, async_created_chat_attachment):
    result = await async_chat_attachments_service.fetch_page(limit=1)

    assert len(result) > 0


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")  # noqa: AAA01
def test_create_chat_attachment(async_created_chat_attachment, chat_attachment_data):
    assert async_created_chat_attachment.id is not None
    assert async_created_chat_attachment.to_dict().get("name") == chat_attachment_data["name"]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_get_chat_attachment(async_chat_attachments_service, async_created_chat_attachment):
    result = await async_chat_attachments_service.get(async_created_chat_attachment.id)

    assert result.id == async_created_chat_attachment.id


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
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


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_download_chat_attachment(
    async_chat_attachments_service, async_created_chat_attachment
):
    result = await async_chat_attachments_service.download(
        async_created_chat_attachment.id,
        accept="application/pdf",
    )

    assert result.file_contents is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_delete_chat_attachment(async_chat_attachments_service, chat_attachment_data, pdf_fd):
    created = await async_chat_attachments_service.create(chat_attachment_data, file=pdf_fd)

    await async_chat_attachments_service.delete(created.id)


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_get_chat_attachment_not_found(
    async_chat_attachments_service, invalid_chat_attachment_id
):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_chat_attachments_service.get(invalid_chat_attachment_id)


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_update_chat_attachment_not_found(
    async_chat_attachments_service, invalid_chat_attachment_id
):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_chat_attachments_service.update(
            invalid_chat_attachment_id,
            {"description": "updated description"},
        )


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_delete_chat_attachment_not_found(
    async_chat_attachments_service, invalid_chat_attachment_id
):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_chat_attachments_service.delete(invalid_chat_attachment_id)
