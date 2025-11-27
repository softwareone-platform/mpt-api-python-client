import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


def test_create_attachment(created_attachment, attachment_data):
    result = created_attachment

    assert result.name == attachment_data["name"]
    assert result.description == attachment_data["description"]


def test_update_attachment(attachment_service, created_attachment):
    update_data = {"name": "Updated e2e test attachment - please delete"}

    result = attachment_service.update(created_attachment.id, update_data)

    assert result.name == update_data["name"]


def test_get_attachment(attachment_service, attachment_id):
    result = attachment_service.get(attachment_id)

    assert result.id == attachment_id


def test_download_attachment(attachment_service, attachment_id):
    result = attachment_service.download(attachment_id)

    assert result.file_contents is not None
    assert result.filename == "empty.pdf"


def test_iterate_attachments(attachment_service, created_attachment):
    result = list(attachment_service.iterate())

    assert any(att.id == created_attachment.id for att in result)


def test_filter_attachments(attachment_service, created_attachment):
    result = list(attachment_service.filter(RQLQuery(id=created_attachment.id)).iterate())

    assert len(result) == 1
    assert result[0].id == created_attachment.id


def test_not_found(attachment_service):
    with pytest.raises(MPTAPIError):
        attachment_service.get("ATT-000-000-000")


def test_delete_attachment(attachment_service, created_attachment):
    attachment_service.delete(created_attachment.id)

    with pytest.raises(MPTAPIError):
        attachment_service.get(created_attachment.id)
