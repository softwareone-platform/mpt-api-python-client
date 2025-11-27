import pytest

from mpt_api_client.resources.billing.billing import AsyncBilling, Billing
from mpt_api_client.resources.billing.credit_memos import (
    AsyncCreditMemosService,
    CreditMemosService,
)
from mpt_api_client.resources.billing.custom_ledgers import (
    AsyncCustomLedgersService,
    CustomLedgersService,
)
from mpt_api_client.resources.billing.invoices import AsyncInvoicesService, InvoicesService
from mpt_api_client.resources.billing.journals import AsyncJournalsService, JournalsService
from mpt_api_client.resources.billing.ledgers import AsyncLedgersService, LedgersService
from mpt_api_client.resources.billing.manual_overrides import (
    AsyncManualOverridesService,
    ManualOverridesService,
)
from mpt_api_client.resources.billing.statements import AsyncStatementsService, StatementsService


@pytest.fixture
def billing(http_client):
    return Billing(http_client=http_client)


@pytest.fixture
def async_billing(async_http_client):
    return AsyncBilling(http_client=async_http_client)


@pytest.mark.parametrize(
    ("property_name", "expected_service_class"),
    [
        ("journals", JournalsService),
        ("ledgers", LedgersService),
        ("statements", StatementsService),
        ("invoices", InvoicesService),
        ("custom_ledgers", CustomLedgersService),
        ("credit_memos", CreditMemosService),
        ("manual_overrides", ManualOverridesService),
    ],
)
def test_billing_properties(billing, property_name, expected_service_class):
    result = getattr(billing, property_name)

    assert isinstance(result, expected_service_class)
    assert result.http_client is billing.http_client


@pytest.mark.parametrize(
    ("property_name", "expected_service_class"),
    [
        ("journals", AsyncJournalsService),
        ("ledgers", AsyncLedgersService),
        ("statements", AsyncStatementsService),
        ("invoices", AsyncInvoicesService),
        ("custom_ledgers", AsyncCustomLedgersService),
        ("credit_memos", AsyncCreditMemosService),
        ("manual_overrides", AsyncManualOverridesService),
    ],
)
def test_async_billing_properties(async_billing, property_name, expected_service_class):
    result = getattr(async_billing, property_name)

    assert isinstance(result, expected_service_class)
    assert result.http_client is async_billing.http_client


def test_billing_initialization(http_client):
    result = Billing(http_client=http_client)

    assert result.http_client is http_client
    assert isinstance(result, Billing)


def test_async_billing_initialization(async_http_client):
    result = AsyncBilling(http_client=async_http_client)

    assert result.http_client is async_http_client
    assert isinstance(result, AsyncBilling)
