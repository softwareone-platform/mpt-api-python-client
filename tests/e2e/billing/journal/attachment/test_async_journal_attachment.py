import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_journal_attachment(
    async_mpt_ops, journal_attachment_factory, billing_journal_id, pdf_fd
):
    new_journal_attachment_request_data = journal_attachment_factory(
        name="E2E Created Journal Attachment",
    )
    journal_attachments = async_mpt_ops.billing.journals.attachments(billing_journal_id)

    created_journal = await journal_attachments.create(
        new_journal_attachment_request_data, file=pdf_fd
    )

    yield created_journal

    try:
        await journal_attachments.delete(created_journal.id)
    except MPTAPIError as error:
        print("TEARDOWN - Unable to delete journal attachment: %s", error.title)  # noqa: WPS421


@pytest.fixture
def journal_attachments(async_mpt_ops, billing_journal_id):
    return async_mpt_ops.billing.journals.attachments(billing_journal_id)


async def test_get_journal_attachment_by_id(journal_attachments, journal_attachment_id):
    result = await journal_attachments.get(journal_attachment_id)

    assert result is not None


async def test_get_journal_attachment_by_id_not_found(
    journal_attachments, invalid_journal_attachment_id
):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await journal_attachments.get(invalid_journal_attachment_id)


async def test_list_journal_attachments(journal_attachments):
    limit = 10

    result = await journal_attachments.fetch_page(limit=limit)

    assert len(result) > 0


async def test_filter_journal_attachments(journal_attachments, journal_attachment_id):
    select_fields = ["-description"]
    filtered_attachments = (
        journal_attachments
        .filter(RQLQuery(id=journal_attachment_id))
        .filter(RQLQuery(name="E2E Seeded Billing Journal Attachment"))
        .select(*select_fields)
    )

    result = [filtered_attachment async for filtered_attachment in filtered_attachments.iterate()]

    assert len(result) == 1


def test_create_billing_journal_attachment(created_journal_attachment):
    result = created_journal_attachment

    assert result is not None


async def test_update_journal_attachment(journal_attachments, created_journal_attachment):
    updated_name = "E2E Updated Journal Attachment Name"
    updated_attachment_data = {
        "name": updated_name,
        "description": updated_name,
    }

    result = await journal_attachments.update(
        created_journal_attachment.id, updated_attachment_data
    )

    assert result is not None


async def test_delete_journal_attachment(journal_attachments, created_journal_attachment):
    result = created_journal_attachment

    await journal_attachments.delete(result.id)


async def test_download_journal_attachment(journal_attachments, journal_attachment_id):
    result = await journal_attachments.download(journal_attachment_id)

    assert result.file_contents is not None
    assert result.filename is not None
