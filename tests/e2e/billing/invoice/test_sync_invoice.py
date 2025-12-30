import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_invoice(mpt_client, invoice_factory):
    new_invoice_request_data = invoice_factory(
        document_number="e2e-invoice-001",
    )
    return mpt_client.billing.invoices.create(new_invoice_request_data)


def test_get_invoice_by_id(mpt_client, created_invoice):
    result = mpt_client.billing.invoices.get(created_invoice.id)

    assert result is not None


def test_get_invoice_by_id_not_found(mpt_client, invalid_invoice_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_client.billing.invoices.get(invalid_invoice_id)


def test_list_invoices(mpt_client):
    limit = 10

    result = mpt_client.billing.invoices.fetch_page(limit=limit)

    assert len(result) > 0


def test_filter_invoices(mpt_client, created_invoice):
    select_fields = ["-agreement"]
    filtered_invoices = (
        mpt_client.billing.invoices
        .filter(RQLQuery(id=created_invoice.id))
        .filter(RQLQuery(countryCode="US"))
        .select(*select_fields)
    )

    result = list(filtered_invoices.iterate())

    assert len(result) == 1


def test_create_invoice(created_invoice):
    result = created_invoice

    assert result is not None
