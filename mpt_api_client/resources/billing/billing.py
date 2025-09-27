from mpt_api_client.http import AsyncHTTPClient, HTTPClient
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


class Billing:
    """Billing MPT API Module."""

    def __init__(self, *, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def journals(self) -> JournalsService:
        """Journals service."""
        return JournalsService(http_client=self.http_client)

    @property
    def ledgers(self) -> LedgersService:
        """Ledgers service."""
        return LedgersService(http_client=self.http_client)

    @property
    def statements(self) -> StatementsService:
        """Statements service."""
        return StatementsService(http_client=self.http_client)

    @property
    def invoices(self) -> InvoicesService:
        """Invoices service."""
        return InvoicesService(http_client=self.http_client)

    @property
    def custom_ledgers(self) -> CustomLedgersService:
        """Custom ledgers service."""
        return CustomLedgersService(http_client=self.http_client)

    @property
    def credit_memos(self) -> CreditMemosService:
        """Credit Memos service."""
        return CreditMemosService(http_client=self.http_client)

    @property
    def manual_overrides(self) -> ManualOverridesService:
        """Manual overrides service."""
        return ManualOverridesService(http_client=self.http_client)


class AsyncBilling:
    """Billing MPT API Module."""

    def __init__(self, *, http_client: AsyncHTTPClient):
        self.http_client = http_client

    @property
    def journals(self) -> AsyncJournalsService:
        """Journals service."""
        return AsyncJournalsService(http_client=self.http_client)

    @property
    def ledgers(self) -> AsyncLedgersService:
        """Ledgers service."""
        return AsyncLedgersService(http_client=self.http_client)

    @property
    def statements(self) -> AsyncStatementsService:
        """Statements service."""
        return AsyncStatementsService(http_client=self.http_client)

    @property
    def invoices(self) -> AsyncInvoicesService:
        """Invoices service."""
        return AsyncInvoicesService(http_client=self.http_client)

    @property
    def custom_ledgers(self) -> AsyncCustomLedgersService:
        """Custom ledgers service."""
        return AsyncCustomLedgersService(http_client=self.http_client)

    @property
    def credit_memos(self) -> AsyncCreditMemosService:
        """Credit Memos service."""
        return AsyncCreditMemosService(http_client=self.http_client)

    @property
    def manual_overrides(self) -> AsyncManualOverridesService:
        """Manual overrides service."""
        return AsyncManualOverridesService(http_client=self.http_client)
