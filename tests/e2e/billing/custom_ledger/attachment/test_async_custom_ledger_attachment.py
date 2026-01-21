import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_custom_ledger_attachment(
    async_mpt_ops, custom_ledger_attachment_factory, custom_ledger_id, pdf_fd
):
    new_custom_ledger_attachment_request_data = custom_ledger_attachment_factory(
        name="E2E Created Custom Ledger Attachment",
    )
    custom_ledger_attachments = async_mpt_ops.billing.custom_ledgers.attachments(custom_ledger_id)

    created_attachment = await custom_ledger_attachments.create(
        new_custom_ledger_attachment_request_data, file=pdf_fd
    )

    yield created_attachment

    try:
        await custom_ledger_attachments.delete(created_attachment.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete custom ledger attachment: {error.title}")  # noqa: WPS421


@pytest.fixture
def custom_ledger_attachments(async_mpt_ops, custom_ledger_id):
    return async_mpt_ops.billing.custom_ledgers.attachments(custom_ledger_id)


async def test_get_custom_ledger_attachment_by_id(
    custom_ledger_attachments, custom_ledger_attachment_id
):
    result = await custom_ledger_attachments.get(custom_ledger_attachment_id)

    assert result is not None


async def test_get_custom_ledger_attachment_by_id_not_found(
    custom_ledger_attachments, invalid_custom_ledger_attachment_id
):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await custom_ledger_attachments.get(invalid_custom_ledger_attachment_id)


async def test_list_custom_ledger_attachments(custom_ledger_attachments):
    limit = 10

    result = await custom_ledger_attachments.fetch_page(limit=limit)

    assert len(result) > 0


async def test_filter_custom_ledger_attachments(
    custom_ledger_attachments, custom_ledger_attachment_id
):
    select_fields = ["-price"]
    filtered_attachments = (
        custom_ledger_attachments
        .filter(RQLQuery(id=custom_ledger_attachment_id))
        .filter(RQLQuery(name="test_custom_ledger.xlsx"))
        .select(*select_fields)
    )

    result = [attachment async for attachment in filtered_attachments.iterate()]

    assert len(result) == 1


def test_create_billing_custom_ledger_attachment(created_custom_ledger_attachment):
    result = created_custom_ledger_attachment

    assert result is not None


async def test_update_billing_custom_ledger_attachment(
    custom_ledger_attachments, created_custom_ledger_attachment
):
    updated_name = "E2E Updated Custom Ledger Attachment"

    update_data = {
        "name": updated_name,
    }

    updated_attachment = await custom_ledger_attachments.update(
        created_custom_ledger_attachment.id,
        update_data,
    )

    assert updated_attachment.name == updated_name


async def test_delete_billing_custom_ledger_attachment(
    custom_ledger_attachments, created_custom_ledger_attachment
):
    result = created_custom_ledger_attachment

    await custom_ledger_attachments.delete(result.id)


async def test_download_billing_custom_ledger_attachment(
    custom_ledger_attachments, created_custom_ledger_attachment
):
    result = await custom_ledger_attachments.download(created_custom_ledger_attachment.id)

    assert result.file_contents is not None
    assert result.filename is not None
