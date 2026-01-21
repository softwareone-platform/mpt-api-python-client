import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_billing_journal(async_mpt_vendor, billing_journal_factory):
    new_billing_journal_request_data = billing_journal_factory(
        name="E2E Created Billing Journal",
    )

    created_billing_journal = await async_mpt_vendor.billing.journals.create(
        new_billing_journal_request_data
    )

    yield created_billing_journal

    try:
        await async_mpt_vendor.billing.journals.delete(created_billing_journal.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete billing journal: {error.title}")  # noqa: WPS421


@pytest.fixture
async def submitted_billing_journal(async_mpt_vendor, created_billing_journal, billing_journal_fd):
    await async_mpt_vendor.billing.journals.submit(created_billing_journal.id)
    await async_mpt_vendor.billing.journals.upload(
        journal_id=created_billing_journal.id,
        file=billing_journal_fd,
    )

    return created_billing_journal


@pytest.fixture
async def completed_billing_journal(async_mpt_vendor, submitted_billing_journal):
    await async_mpt_vendor.billing.journals.accept(submitted_billing_journal.id)
    await async_mpt_vendor.billing.journals.complete(submitted_billing_journal.id)
    return submitted_billing_journal


async def test_get_billing_journal_by_id(async_mpt_vendor, billing_journal_id):
    result = await async_mpt_vendor.billing.journals.get(billing_journal_id)

    assert result is not None


async def test_list_billing_journals(async_mpt_vendor):
    limit = 10

    result = await async_mpt_vendor.billing.journals.fetch_page(limit=limit)

    assert len(result) > 0


async def test_get_billing_journal_by_id_not_found(async_mpt_vendor, invalid_billing_journal_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_vendor.billing.journals.get(invalid_billing_journal_id)


async def test_filter_billing_journals(async_mpt_vendor, billing_journal_id):
    select_fields = ["-value"]
    filtered_billing_journals = (
        async_mpt_vendor.billing.journals
        .filter(RQLQuery(id=billing_journal_id))
        .filter(RQLQuery(name="E2E Seeded Billing Journal"))
        .select(*select_fields)
    )

    result = [billing_journal async for billing_journal in filtered_billing_journals.iterate()]

    assert len(result) == 1


def test_create_billing_journal(created_billing_journal):
    result = created_billing_journal

    assert result is not None


async def test_update_billing_journal(
    async_mpt_vendor, created_billing_journal, billing_journal_factory
):
    updated_name = "E2E Updated Billing Journal Name"
    updated_billing_journal_data = billing_journal_factory(name=updated_name)

    result = await async_mpt_vendor.billing.journals.update(
        created_billing_journal.id,
        updated_billing_journal_data,
    )

    assert result.name == updated_name


async def test_delete_billing_journal(async_mpt_vendor, created_billing_journal):
    result = created_billing_journal

    await async_mpt_vendor.billing.journals.delete(result.id)


async def test_upload_billing_journal(
    async_mpt_vendor, created_billing_journal, billing_journal_fd
):
    result = await async_mpt_vendor.billing.journals.upload(
        journal_id=created_billing_journal.id,
        file=billing_journal_fd,
    )

    assert result is not None
