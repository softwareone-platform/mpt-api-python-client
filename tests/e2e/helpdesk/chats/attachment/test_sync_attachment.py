import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_list_chat_attachments(chat_attachments_service, created_chat_attachment):
    result = chat_attachments_service.fetch_page(limit=1)

    assert len(result) > 0


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")  # noqa: AAA01
def test_create_chat_attachment(created_chat_attachment, chat_attachment_data):
    assert created_chat_attachment.id is not None
    assert created_chat_attachment.to_dict().get("name") == chat_attachment_data["name"]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_get_chat_attachment(chat_attachments_service, created_chat_attachment):
    result = chat_attachments_service.get(created_chat_attachment.id)

    assert result.id == created_chat_attachment.id


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_update_chat_attachment(chat_attachments_service, created_chat_attachment, short_uuid):
    updated_name = f"e2e updated attachment - {short_uuid}"

    result = chat_attachments_service.update(
        created_chat_attachment.id,
        {"name": updated_name, "description": updated_name},
    )

    assert result.id == created_chat_attachment.id
    assert result.to_dict().get("name") == updated_name


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_download_chat_attachment(chat_attachments_service, created_chat_attachment):
    result = chat_attachments_service.download(created_chat_attachment.id, accept="application/pdf")

    assert result.file_contents is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")  # noqa: AAA01
def test_delete_chat_attachment(chat_attachments_service, chat_attachment_data, pdf_fd):
    created = chat_attachments_service.create(chat_attachment_data, file=pdf_fd)

    chat_attachments_service.delete(created.id)


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_get_chat_attachment_not_found(chat_attachments_service, invalid_chat_attachment_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        chat_attachments_service.get(invalid_chat_attachment_id)


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_update_chat_attachment_not_found(chat_attachments_service, invalid_chat_attachment_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        chat_attachments_service.update(
            invalid_chat_attachment_id,
            {"description": "updated description"},
        )


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_delete_chat_attachment_not_found(chat_attachments_service, invalid_chat_attachment_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        chat_attachments_service.delete(invalid_chat_attachment_id)
