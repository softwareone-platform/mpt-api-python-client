import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def invoices(mpt_ops):
    limit = 1
    return mpt_ops.billing.invoices.fetch_page(limit=limit)


@pytest.fixture
def invoice(invoices):
    if invoices:
        return invoices[0]
    return None


def test_get_invoice_by_id(mpt_ops, invoice):
    if invoice is None:
        pytest.skip("No invoice available for get by id test.")
    invoice_id = invoice.id

    result = mpt_ops.billing.invoices.get(invoice_id)

    assert result is not None


def test_get_invoice_by_id_not_found(mpt_ops, invalid_invoice_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.billing.invoices.get(invalid_invoice_id)


def test_list_invoices(mpt_ops):
    limit = 10

    result = mpt_ops.billing.invoices.fetch_page(limit=limit)

    assert len(result) > 0


def test_filter_invoices(mpt_ops, invoice):
    if invoice is None:
        pytest.skip("No invoice available for filtering test.")
    invoice_id = invoice.id
    invoice_status = invoice.status
    select_fields = ["-buyer"]
    filtered_invoices = (
        mpt_ops.billing.invoices.filter(RQLQuery(id=invoice_id))
        .filter(RQLQuery(status=invoice_status))
        .select(*select_fields)
    )

    result = list(filtered_invoices.iterate())

    assert len(result) == 1
