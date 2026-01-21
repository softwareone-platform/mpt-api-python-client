import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def invoices(async_mpt_ops):
    limit = 1
    return await async_mpt_ops.billing.invoices.fetch_page(limit=limit)


@pytest.fixture
def invoice(invoices):
    if invoices:
        return invoices[0]
    return None


async def test_get_invoice_by_id(async_mpt_ops, invoice):
    if invoice is None:
        pytest.skip("No invoice available for get by id test.")
    invoice_id = invoice.id

    result = await async_mpt_ops.billing.invoices.get(invoice_id)

    assert result is not None


async def test_get_invoice_by_id_not_found(async_mpt_ops, invalid_invoice_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.billing.invoices.get(invalid_invoice_id)


async def test_list_invoices(async_mpt_ops):
    limit = 10

    result = await async_mpt_ops.billing.invoices.fetch_page(limit=limit)

    assert len(result) > 0


async def test_filter_invoices(async_mpt_ops, invoice):
    if invoice is None:
        pytest.skip("No invoice available to test filtering.")
    invoice_id = invoice.id
    invoice_status = invoice.status
    select_fields = ["-buyer"]
    filtered_invoices = (
        async_mpt_ops.billing.invoices
        .filter(RQLQuery(id=invoice_id))
        .filter(RQLQuery(status=invoice_status))
        .select(*select_fields)
    )

    result = [invoice async for invoice in filtered_invoices.iterate()]

    assert len(result) == 1
