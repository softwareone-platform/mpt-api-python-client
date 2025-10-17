from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.billing.custom_ledger_attachments import (
    AsyncCustomLedgerAttachmentsService,
    CustomLedgerAttachmentsService,
)
from mpt_api_client.resources.billing.custom_ledger_charges import (
    AsyncCustomLedgerChargesService,
    CustomLedgerChargesService,
)
from mpt_api_client.resources.billing.custom_ledger_upload import (
    AsyncCustomLedgerUploadService,
    CustomLedgerUploadService,
)
from mpt_api_client.resources.billing.mixins import AcceptableMixin, AsyncAcceptableMixin


class CustomLedger(Model):
    """Custom Ledger resource."""


class CustomLedgersServiceConfig:
    """Custom Ledgers service configuration."""

    _endpoint = "/public/v1/billing/custom-ledgers"
    _model_class = CustomLedger
    _collection_key = "data"


class CustomLedgersService(
    ManagedResourceMixin[CustomLedger],
    CollectionMixin[CustomLedger],
    AcceptableMixin[CustomLedger],
    Service[CustomLedger],
    CustomLedgersServiceConfig,
):
    """Custom Ledgers service."""

    def charges(self, custom_ledger_id: str) -> CustomLedgerChargesService:
        """Return custom ledger charges service."""
        return CustomLedgerChargesService(
            http_client=self.http_client,
            endpoint_params={"custom_ledger_id": custom_ledger_id},
        )

    def upload(self, custom_ledger_id: str) -> CustomLedgerUploadService:
        """Get the Custom Ledger Upload service."""
        return CustomLedgerUploadService(
            http_client=self.http_client,
            endpoint_params={"custom_ledger_id": custom_ledger_id},
        )

    def attachments(self, custom_ledger_id: str) -> CustomLedgerAttachmentsService:
        """Return custom ledger attachments service."""
        return CustomLedgerAttachmentsService(
            http_client=self.http_client,
            endpoint_params={"custom_ledger_id": custom_ledger_id},
        )


class AsyncCustomLedgersService(
    AsyncManagedResourceMixin[CustomLedger],
    AsyncCollectionMixin[CustomLedger],
    AsyncAcceptableMixin[CustomLedger],
    AsyncService[CustomLedger],
    CustomLedgersServiceConfig,
):
    """Async Custom Ledgers service."""

    def charges(self, custom_ledger_id: str) -> AsyncCustomLedgerChargesService:
        """Return custom ledger charges service."""
        return AsyncCustomLedgerChargesService(
            http_client=self.http_client,
            endpoint_params={"custom_ledger_id": custom_ledger_id},
        )

    def upload(self, custom_ledger_id: str) -> AsyncCustomLedgerUploadService:
        """Get the Async Custom Ledger Upload service."""
        return AsyncCustomLedgerUploadService(
            http_client=self.http_client,
            endpoint_params={"custom_ledger_id": custom_ledger_id},
        )

    def attachments(self, custom_ledger_id: str) -> AsyncCustomLedgerAttachmentsService:
        """Return custom ledger attachments service."""
        return AsyncCustomLedgerAttachmentsService(
            http_client=self.http_client,
            endpoint_params={"custom_ledger_id": custom_ledger_id},
        )
