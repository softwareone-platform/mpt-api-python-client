import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_ledger_attachment(async_mpt_ops, ledger_attachment_factory, ledger_id, pdf_fd):
    new_ledger_attachment_request_data = ledger_attachment_factory(
        name="E2E Seeded Ledger Attachment",
    )
    ledger_attachments = async_mpt_ops.billing.ledgers.attachments(ledger_id)
    created_ledger_attachment = await ledger_attachments.create(
        new_ledger_attachment_request_data, file=pdf_fd
    )

    yield created_ledger_attachment

    try:
        await ledger_attachments.delete(created_ledger_attachment.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete ledger attachment: {error.title}")


@pytest.fixture
def ledger_attachments(async_mpt_ops, ledger_id):
    return async_mpt_ops.billing.ledgers.attachments(ledger_id)


async def test_get_ledger_attachment_by_id(ledger_attachments, ledger_attachment_id):
    result = await ledger_attachments.get(ledger_attachment_id)

    assert result is not None


async def test_get_ledger_attachment_by_id_not_found(
    ledger_attachments, invalid_ledger_attachment_id
):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await ledger_attachments.get(invalid_ledger_attachment_id)


async def test_list_ledger_attachments(ledger_attachments):
    limit = 10

    result = await ledger_attachments.fetch_page(limit=limit)

    assert len(result) > 0


async def test_filter_ledger_attachments(ledger_attachments, ledger_attachment_id):
    select_fields = ["-description"]
    filtered_attachments = (
        ledger_attachments.filter(RQLQuery(id=ledger_attachment_id))
        .filter(RQLQuery(name="E2E Seeded Ledger Attachment"))
        .select(*select_fields)
    )

    result = [attachment async for attachment in filtered_attachments.iterate()]

    assert len(result) > 0


def test_create_billing_ledger_attachment(created_ledger_attachment):
    result = created_ledger_attachment

    assert result is not None


async def test_update_billing_ledger_attachment(
    ledger_attachments, created_ledger_attachment, ledger_attachment_factory
):
    updated_data = ledger_attachment_factory(
        name="E2E Updated Ledger Attachment",
    )

    result = await ledger_attachments.update(created_ledger_attachment.id, updated_data)

    assert result is not None


async def test_delete_billing_ledger_attachment(ledger_attachments, created_ledger_attachment):
    result = created_ledger_attachment

    await ledger_attachments.delete(result.id)


async def test_download_billing_ledger_attachment(ledger_attachments, ledger_attachment_id):
    result = await ledger_attachments.download(ledger_attachment_id)

    assert result.file_contents is not None
    assert result.filename is not None
