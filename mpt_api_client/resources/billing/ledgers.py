from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateMixin,
    AsyncGetMixin,
    CollectionMixin,
    CreateMixin,
    GetMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.billing.ledger_attachments import (
    AsyncLedgerAttachmentsService,
    LedgerAttachmentsService,
)
from mpt_api_client.resources.billing.ledger_charges import (
    AsyncLedgerChargesService,
    LedgerChargesService,
)


class Ledger(Model):
    """Ledger resource."""


class LedgersServiceConfig:
    """Ledgers service configuration."""

    _endpoint = "/public/v1/billing/ledgers"
    _model_class = Ledger
    _collection_key = "data"


class LedgersService(
    CreateMixin[Ledger],
    GetMixin[Ledger],
    CollectionMixin[Ledger],
    Service[Ledger],
    LedgersServiceConfig,
):
    """Ledgers service."""

    def charges(self, ledger_id: str) -> LedgerChargesService:
        """Return ledger charges service."""
        return LedgerChargesService(
            http_client=self.http_client,
            endpoint_params={"ledger_id": ledger_id},
        )

    def attachments(self, ledger_id: str) -> LedgerAttachmentsService:
        """Return ledger attachments service."""
        return LedgerAttachmentsService(
            http_client=self.http_client,
            endpoint_params={"ledger_id": ledger_id},
        )


class AsyncLedgersService(
    AsyncCreateMixin[Ledger],
    AsyncGetMixin[Ledger],
    AsyncCollectionMixin[Ledger],
    AsyncService[Ledger],
    LedgersServiceConfig,
):
    """Async Ledgers service."""

    def charges(self, ledger_id: str) -> AsyncLedgerChargesService:
        """Return ledger charges service."""
        return AsyncLedgerChargesService(
            http_client=self.http_client,
            endpoint_params={"ledger_id": ledger_id},
        )

    def attachments(self, ledger_id: str) -> AsyncLedgerAttachmentsService:
        """Return ledger attachments service."""
        return AsyncLedgerAttachmentsService(
            http_client=self.http_client,
            endpoint_params={"ledger_id": ledger_id},
        )
