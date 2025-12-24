from urllib.parse import urljoin

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.http.types import FileTypes
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
    _upload_file_key = "file"
    _upload_data_key = "id"


class JournalsService(
    RegeneratableMixin[Journal],
    ManagedResourceMixin[Journal],
    CollectionMixin[Journal],
    Service[Journal],
    JournalsServiceConfig,
):
    """Journals service."""

    def upload(self, journal_id: str, file: FileTypes | None = None) -> Journal:  # noqa: WPS110
        """Upload journal file.

        Args:
            journal_id: Journal ID.
            file: journal file.

        Returns:
            Journal: Created resource.
        """
        files = {}

        if file:
            files[self._upload_file_key] = file  # UNUSED type: ignore[attr-defined]
            files[self._upload_data_key] = journal_id  # UNUSED type: ignore

        path = urljoin(f"{self.path}/", f"{journal_id}/upload")

        response = self.http_client.request(  # UNUSED type: ignore[attr-defined]
            "post",
            path,  # UNUSED type: ignore[attr-defined]
            files=files,
            force_multipart=True,
        )

        return self._model_class.from_response(
            response
        )  # UNUSED type: ignore[attr-defined, no-any-return]

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
    AsyncRegeneratableMixin[Journal],
    AsyncManagedResourceMixin[Journal],
    AsyncCollectionMixin[Journal],
    AsyncService[Journal],
    JournalsServiceConfig,
):
    """Async Journals service."""

    async def upload(self, journal_id: str, file: FileTypes | None = None) -> Journal:  # noqa: WPS110
        """Upload journal file.

        Args:
            journal_id: Journal ID.
            file: journal file.

        Returns:
            Journal: Created resource.
        """
        files = {}

        if file:
            files[self._upload_file_key] = file  # UNUSED type: ignore[attr-defined]
            files[self._upload_data_key] = journal_id  # UNUSED type: ignore

        path = urljoin(f"{self.path}/", f"{journal_id}/upload")

        response = await self.http_client.request(  # UNUSED type: ignore[attr-defined]
            "post",
            path,  # UNUSED type: ignore[attr-defined]
            files=files,
            force_multipart=True,
        )

        return self._model_class.from_response(
            response
        )  # UNUSED type: ignore[attr-defined, no-any-return]

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
