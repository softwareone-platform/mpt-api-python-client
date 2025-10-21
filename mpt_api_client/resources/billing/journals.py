from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.billing.journal_attachments import (
    AsyncJournalAttachmentsService,
    JournalAttachmentsService,
)
from mpt_api_client.resources.billing.journal_charges import (
    AsyncJournalChargesService,
    JournalChargesService,
)
from mpt_api_client.resources.billing.journal_sellers import (
    AsyncJournalSellersService,
    JournalSellersService,
)
from mpt_api_client.resources.billing.journal_upload import (
    AsyncJournalUploadService,
    JournalUploadService,
)
from mpt_api_client.resources.billing.mixins import AsyncRegeneratableMixin, RegeneratableMixin


class Journal(Model):
    """Journal resource."""


class JournalsServiceConfig:
    """Journals service configuration."""

    _endpoint = "/public/v1/billing/journals"
    _model_class = Journal
    _collection_key = "data"


class JournalsService(
    RegeneratableMixin[Journal],
    ManagedResourceMixin[Journal],
    CollectionMixin[Journal],
    Service[Journal],
    JournalsServiceConfig,
):
    """Journals service."""

    def attachments(self, journal_id: str) -> JournalAttachmentsService:
        """Return journal attachments service."""
        return JournalAttachmentsService(
            http_client=self.http_client,
            endpoint_params={"journal_id": journal_id},
        )

    def sellers(self, journal_id: str) -> JournalSellersService:
        """Return journal sellers service."""
        return JournalSellersService(
            http_client=self.http_client, endpoint_params={"journal_id": journal_id}
        )

    def charges(self, journal_id: str) -> JournalChargesService:
        """Return journal charges service."""
        return JournalChargesService(
            http_client=self.http_client, endpoint_params={"journal_id": journal_id}
        )

    def upload(self, journal_id: str) -> JournalUploadService:
        """Return journal upload service."""
        return JournalUploadService(
            http_client=self.http_client, endpoint_params={"journal_id": journal_id}
        )


class AsyncJournalsService(
    AsyncRegeneratableMixin[Journal],
    AsyncManagedResourceMixin[Journal],
    AsyncCollectionMixin[Journal],
    AsyncService[Journal],
    JournalsServiceConfig,
):
    """Async Journals service."""

    def attachments(self, journal_id: str) -> AsyncJournalAttachmentsService:
        """Return journal attachments service."""
        return AsyncJournalAttachmentsService(
            http_client=self.http_client,
            endpoint_params={"journal_id": journal_id},
        )

    def sellers(self, journal_id: str) -> AsyncJournalSellersService:
        """Return journal sellers service."""
        return AsyncJournalSellersService(
            http_client=self.http_client, endpoint_params={"journal_id": journal_id}
        )

    def charges(self, journal_id: str) -> AsyncJournalChargesService:
        """Return journal charges service."""
        return AsyncJournalChargesService(
            http_client=self.http_client, endpoint_params={"journal_id": journal_id}
        )

    def upload(self, journal_id: str) -> AsyncJournalUploadService:
        """Return journal upload service."""
        return AsyncJournalUploadService(
            http_client=self.http_client, endpoint_params={"journal_id": journal_id}
        )
