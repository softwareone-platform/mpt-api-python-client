import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_credit_memo_attachment(
    mpt_ops, credit_memo_attachment_factory, billing_credit_memo_id, pdf_fd
):
    new_credit_memo_attachment_request_data = credit_memo_attachment_factory(
        name="E2E Created Credit Memo Attachment",
    )
    credit_memo_attachments = mpt_ops.billing.credit_memos.attachments(billing_credit_memo_id)

    created_credit_memo = credit_memo_attachments.create(
        new_credit_memo_attachment_request_data, file=pdf_fd
    )

    yield created_credit_memo

    try:
        credit_memo_attachments.delete(created_credit_memo.id)
    except MPTAPIError as error:
        print("TEARDOWN - Unable to delete credit memo attachment: %s", error.title)  # noqa: WPS421


@pytest.fixture
def credit_memo_attachments(mpt_ops, billing_credit_memo_id):
    return mpt_ops.billing.credit_memos.attachments(billing_credit_memo_id)


def test_get_credit_memo_attachment_by_id(credit_memo_attachments, credit_memo_attachment_id):
    result = credit_memo_attachments.get(credit_memo_attachment_id)

    assert result is not None


def test_get_credit_memo_attachment_by_id_not_found(
    credit_memo_attachments, invalid_credit_memo_attachment_id
):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        credit_memo_attachments.get(invalid_credit_memo_attachment_id)


def test_list_credit_memo_attachments(credit_memo_attachments):
    limit = 10

    result = credit_memo_attachments.fetch_page(limit=limit)

    assert len(result) > 0


def test_filter_credit_memo_attachments(credit_memo_attachments, credit_memo_attachment_id):
    select_fields = ["-description"]
    filtered_attachments = (
        credit_memo_attachments.filter(RQLQuery(id=credit_memo_attachment_id))
        .filter(RQLQuery(name="E2E Seeded Billing Credit Memo Attachment"))
        .select(*select_fields)
    )

    result = list(filtered_attachments.iterate())

    assert len(result) == 1


def test_create_billing_credit_memo_attachment(created_credit_memo_attachment):
    result = created_credit_memo_attachment

    assert result is not None


def test_download_billing_credit_memo_attachment(credit_memo_attachments, credit_memo_attachment_id):
    result = credit_memo_attachments.download(credit_memo_attachment_id)

    assert result is not None


def test_update_credit_memo_attachment(credit_memo_attachments, created_credit_memo_attachment):
    updated_name = "E2E Updated Credit Memo Attachment Name"
    updated_attachment_data = {
        "name": updated_name,
        "description": updated_name,
    }

    result = credit_memo_attachments.update(created_credit_memo_attachment.id, updated_attachment_data)

    assert result.name == updated_name


def test_delete_credit_memo_attachment(credit_memo_attachments, created_credit_memo_attachment):
    result = created_credit_memo_attachment

    credit_memo_attachments.delete(result.id)
