from mpt_api_client.http import AsyncService, CreateMixin, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncUpdateMixin,
    DeleteMixin,
    UpdateMixin,
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
from mpt_api_client.resources.billing.mixins import AsyncRegeneratableMixin, RegeneratableMixin


class Journal(Model):
    """Journal resource."""


class JournalsServiceConfig:
    """Journals service configuration."""

    _endpoint = "/public/v1/billing/journals"
    _model_class = Journal
    _collection_key = "data"


class JournalsService(
    CreateMixin[Journal],
    DeleteMixin,
    UpdateMixin[Journal],
    RegeneratableMixin[Journal],
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


class AsyncJournalsService(
    AsyncCreateMixin[Journal],
    AsyncDeleteMixin,
    AsyncUpdateMixin[Journal],
    AsyncRegeneratableMixin[Journal],
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
