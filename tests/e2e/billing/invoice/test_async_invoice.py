import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_invoice(async_mpt_client, invoice_factory):
    new_invoice_request_data = invoice_factory(
        document_number="e2e-invoice-001",
    )
    return await async_mpt_client.billing.invoices.create(new_invoice_request_data)


async def test_get_invoice_by_id(async_mpt_client, created_invoice):
    result = await async_mpt_client.billing.invoices.get(created_invoice.id)

    assert result is not None


async def test_get_invoice_by_id_not_found(async_mpt_client, invalid_invoice_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_client.billing.invoices.get(invalid_invoice_id)


async def test_list_invoices(async_mpt_client):
    limit = 10

    result = await async_mpt_client.billing.invoices.fetch_page(limit=limit)

    assert len(result) > 0


async def test_filter_invoices(async_mpt_client, created_invoice):
    select_fields = ["-agreement"]
    filtered_invoices = (
        async_mpt_client.billing.invoices
            .filter(RQLQuery(id=created_invoice.id))
            .filter(RQLQuery(countryCode="US"))
            .select(*select_fields)
    )

    result = [invoice async for invoice in filtered_invoices.iterate()]

    assert len(result) == 1


async def test_create_invoice(created_invoice):
    result = created_invoice

    assert result is not None
