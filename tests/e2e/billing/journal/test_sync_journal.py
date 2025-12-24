import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_billing_journal(mpt_vendor, billing_journal_factory):
    new_billing_journal_request_data = billing_journal_factory(
        name="E2E Created Billing Journal",
    )

    created_billing_journal = mpt_vendor.billing.journals.create(new_billing_journal_request_data)

    yield created_billing_journal

    try:
        mpt_vendor.billing.journals.delete(created_billing_journal.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete billing journal: {error.title}")  # noqa: WPS421


@pytest.fixture
def submitted_billing_journal(mpt_vendor, created_billing_journal, billing_journal_fd):
    mpt_vendor.billing.journals.submit(created_billing_journal.id)
    mpt_vendor.billing.journals.upload(
        journal_id=created_billing_journal.id,
        file=billing_journal_fd,
    )

    return created_billing_journal


@pytest.fixture
def completed_billing_journal(mpt_vendor, submitted_billing_journal):
    mpt_vendor.billing.journals.accept(submitted_billing_journal.id)
    mpt_vendor.billing.journals.complete(submitted_billing_journal.id)
    return submitted_billing_journal


def test_get_billing_journal_by_id(mpt_vendor, billing_journal_id):
    result = mpt_vendor.billing.journals.get(billing_journal_id)

    assert result is not None


def test_list_billing_journals(mpt_vendor):
    limit = 10

    result = mpt_vendor.billing.journals.fetch_page(limit=limit)

    assert len(result) > 0


def test_get_billing_journal_by_id_not_found(mpt_vendor, invalid_billing_journal_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_vendor.billing.journals.get(invalid_billing_journal_id)


def test_filter_billing_journals(mpt_vendor, billing_journal_id):
    select_fields = ["-value"]
    filtered_billing_journals = (
        mpt_vendor.billing.journals.filter(RQLQuery(id=billing_journal_id))
        .filter(RQLQuery(name="E2E Seeded Billing Journal"))
        .select(*select_fields)
    )

    result = list(filtered_billing_journals.iterate())

    assert len(result) == 1


def test_create_billing_journal(created_billing_journal):
    result = created_billing_journal

    assert result is not None


def test_update_billing_journal(mpt_vendor, created_billing_journal, billing_journal_factory):
    updated_name = "E2E Updated Billing Journal Name"
    updated_billing_journal_data = billing_journal_factory(name=updated_name)

    result = mpt_vendor.billing.journals.update(
        created_billing_journal.id,
        updated_billing_journal_data,
    )

    assert result.name == updated_name


def test_delete_billing_journal(mpt_vendor, created_billing_journal):
    result = created_billing_journal

    mpt_vendor.billing.journals.delete(result.id)


def test_upload_billing_journal(mpt_vendor, created_billing_journal, billing_journal_fd):
    result = mpt_vendor.billing.journals.upload(
        journal_id=created_billing_journal.id,
        file=billing_journal_fd,
    )

    assert result is not None
