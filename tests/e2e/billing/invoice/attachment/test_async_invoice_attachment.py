import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_invoice_attachment(
    async_mpt_ops,
    invoice_attachments,
    invoice_attachment_factory,
    pdf_fd,
):
    new_invoice_attachment_request_data = invoice_attachment_factory(
        name="E2E Created Invoice Attachment",
    )

    created_invoice_attachment = invoice_attachments.create(
        new_invoice_attachment_request_data,
        file=pdf_fd,
    )

    yield created_invoice_attachment

    try:
        invoice_attachments.delete(created_invoice_attachment.id)
    except MPTAPIError as error:
        print("TEARDOWN - Unable to delete invoice attachment: %s", error.title)  # noqa: WPS421


@pytest.fixture
async def invoice_attachments(async_mpt_ops, billing_invoice_id):
    return await async_mpt_ops.billing.invoices.attachments(billing_invoice_id)


async def test_get_invoice_attachment_by_id(invoice_attachments, invoice_attachment_id):
    result = await invoice_attachments.get(invoice_attachment_id)
    assert result is not None


async def test_get_invoice_attachment_by_id_not_found(
    invoice_attachments,
    invalid_invoice_attachment_id,
):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await invoice_attachments.get(invalid_invoice_attachment_id)


async def test_list_invoice_attachments(invoice_attachments):
    limit = 10

    result = await invoice_attachments.fetch_page(limit=limit)

    assert len(result) > 0


async def test_filter_invoice_attachments(invoice_attachments, invoice_attachment_id):
    select_fields = ["-description"]
    filtered_attachments = (
        invoice_attachments.filter(RQLQuery(id=invoice_attachment_id))
        .filter(RQLQuery(name="E2E Seeded Billing Invoice Attachment"))
        .select(*select_fields)
    )

    result = [attachment async for attachment in filtered_attachments.iterate()]

    assert len(result) > 0


def test_create_billing_invoice_attachment(created_invoice_attachment):
    result = created_invoice_attachment

    assert result is not None


async def test_update_billing_invoice_attachment(
    invoice_attachments,
    created_invoice_attachment,
):
    update_data = {
        "name": "Updated E2E Invoice Attachment",
        "description": "Updated E2E Invoice Attachment",
    }

    result = await invoice_attachments.update(
        created_invoice_attachment.id,
        update_data,
    )

    assert result is not None


async def test_delete_billing_invoice_attachment(
    invoice_attachments,
    created_invoice_attachment,
):
    result = created_invoice_attachment

    await invoice_attachments.delete(result.id)


async def test_download_billing_invoice_attachment(
    invoice_attachments,
    invoice_attachment_id,
):
    result = await invoice_attachments.download(invoice_attachment_id)

    assert result.file_contents is not None
    assert result.filename is not None
