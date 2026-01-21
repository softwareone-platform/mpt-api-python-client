import pytest

from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def journal_sellers(mpt_vendor, billing_journal_id):
    # Note: relies on seeded e2e config for `billing_journal_id`
    # (see e2e_config.test.json). Update seeds if this changes.
    return mpt_vendor.billing.journals.sellers(billing_journal_id)


def test_list_journal_sellers(journal_sellers):
    limit = 10

    result = journal_sellers.fetch_page(limit=limit)

    assert len(result) > 0


def test_filter_journal_sellers(journal_sellers, seller_id):
    select_fields = ["-period"]
    filtered_sellers = (
        journal_sellers
        .filter(RQLQuery(id=seller_id))
        .filter(RQLQuery(name="E2E Seeded Seller"))
        .select(*select_fields)
    )

    result = list(filtered_sellers.iterate())

    assert len(result) == 1
