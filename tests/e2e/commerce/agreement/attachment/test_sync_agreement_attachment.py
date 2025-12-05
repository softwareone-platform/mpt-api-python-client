import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_agreement_attachment(mpt_ops, agreement_attachment_factory, agreement_id, pdf_fd):
    new_agreement_attachment_request_data = agreement_attachment_factory(
        name="E2E Created Agreement Attachment",
    )
    agreement_attachments = mpt_ops.commerce.agreements.attachments(agreement_id)
    return agreement_attachments.create(new_agreement_attachment_request_data, file=pdf_fd)


@pytest.fixture
def agreement_attachments(mpt_ops, agreement_id):
    return mpt_ops.commerce.agreements.attachments(agreement_id)


def test_get_agreement_attachment_by_id(agreement_attachments, agreement_attachment_id):
    result = agreement_attachments.get(agreement_attachment_id)

    assert result is not None


def test_get_agreement_attachment_by_id_not_found(
    agreement_attachments, invalid_agreement_attachment_id
):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        agreement_attachments.get(invalid_agreement_attachment_id)


def test_list_agreement_attachments(agreement_attachments):
    limit = 10

    result = agreement_attachments.fetch_page(limit=limit)

    assert len(result) > 0


def test_filter_agreement_attachments(agreement_attachments, agreement_attachment_id):
    select_fields = ["-description"]
    filtered_attachments = (
        agreement_attachments.filter(RQLQuery(id=agreement_attachment_id))
        .filter(RQLQuery(name="E2E Seeded Agreement Attachment"))
        .select(*select_fields)
    )

    result = list(filtered_attachments.iterate())

    assert len(result) == 1


def test_create_order_agreement_attachment(created_agreement_attachment):
    result = created_agreement_attachment

    assert result is not None


def test_update_agreement_attachment(agreement_attachments, created_agreement_attachment):
    updated_name = "E2E Updated Agreement Attachment Name"
    updated_attachment_data = {
        "name": updated_name,
        "description": updated_name,
    }

    result = agreement_attachments.update(created_agreement_attachment.id, updated_attachment_data)

    assert result is not None


def test_delete_agreement_attachment(agreement_attachments, created_agreement_attachment):
    result = created_agreement_attachment

    agreement_attachments.delete(result.id)


def test_download_agreement_attachment(agreement_attachments, created_agreement_attachment):
    result = agreement_attachments.download(created_agreement_attachment.id)

    assert result.file_contents is not None
    assert result.filename == "empty.pdf"
