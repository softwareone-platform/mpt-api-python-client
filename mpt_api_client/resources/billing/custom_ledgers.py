import pathlib
from typing import cast
from urllib.parse import urljoin

from mpt_api_client.constants import MIMETYPE_EXCEL_XLSX
from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.http.types import FileContent, FileTypes
from mpt_api_client.models import Model
from mpt_api_client.resources.billing.custom_ledger_attachments import (
    AsyncCustomLedgerAttachmentsService,
    CustomLedgerAttachmentsService,
)
from mpt_api_client.resources.billing.custom_ledger_charges import (
    AsyncCustomLedgerChargesService,
    CustomLedgerChargesService,
)
from mpt_api_client.resources.billing.mixins import AcceptableMixin, AsyncAcceptableMixin


class CustomLedger(Model):
    """Custom Ledger resource."""


class CustomLedgersServiceConfig:
    """Custom Ledgers service configuration."""

    _endpoint = "/public/v1/billing/custom-ledgers"
    _model_class = CustomLedger
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "id"


class CustomLedgersService(
    ManagedResourceMixin[CustomLedger],
    CollectionMixin[CustomLedger],
    AcceptableMixin[CustomLedger],
    Service[CustomLedger],
    CustomLedgersServiceConfig,
):
    """Custom Ledgers service."""

    def upload(self, custom_ledger_id: str, file: FileTypes) -> CustomLedger:
        """Upload custom ledger file.

        Args:
            custom_ledger_id: Custom Ledger ID.
            file: Custom Ledger file.

        Returns:
            CustomLedger: Created resource.
        """
        files: dict[str, FileTypes] = {}

        filename = pathlib.Path(getattr(file, "name", "uploaded_file.xlsx")).name

        # Mimetype is set to Excel XLSX to prevent 415 response from the server
        files[self._upload_file_key] = (
            filename,
            cast("FileContent", file),
            MIMETYPE_EXCEL_XLSX,
        )  # UNUSED type: ignore[attr-defined]
        files[self._upload_data_key] = custom_ledger_id  # UNUSED type: ignore

        path = urljoin(f"{self.path}/", f"{custom_ledger_id}/upload")

        response = self.http_client.request(  # UNUSED type: ignore[attr-defined]
            "post",
            path,  # UNUSED type: ignore[attr-defined]
            files=files,
            force_multipart=True,
        )

        return self._model_class.from_response(
            response
        )  # UNUSED type: ignore[attr-defined, no-any-return]

    def charges(self, custom_ledger_id: str) -> CustomLedgerChargesService:
        """Return custom ledger charges service."""
        return CustomLedgerChargesService(
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

    async def upload(self, custom_ledger_id: str, file: FileTypes) -> CustomLedger:
        """Upload custom ledger file.

        Args:
            custom_ledger_id: Custom Ledger ID.
            file: Custom Ledger file.

        Returns:
            CustomLedger: Created resource.
        """
        files: dict[str, FileTypes] = {}

        filename = pathlib.Path(getattr(file, "name", "uploaded_file.xlsx")).name

        # Mimetype is set to Excel XLSX to prevent 415 response from the server
        files[self._upload_file_key] = (
            filename,
            cast("FileContent", file),
            MIMETYPE_EXCEL_XLSX,
        )  # UNUSED type: ignore[attr-defined]
        files[self._upload_data_key] = custom_ledger_id  # UNUSED type: ignore

        path = urljoin(f"{self.path}/", f"{custom_ledger_id}/upload")

        response = await self.http_client.request(  # UNUSED type: ignore[attr-defined]
            "post",
            path,  # UNUSED type: ignore[attr-defined]
            files=files,
            force_multipart=True,
        )

        return self._model_class.from_response(
            response
        )  # UNUSED type: ignore[attr-defined, no-any-return]

    def charges(self, custom_ledger_id: str) -> AsyncCustomLedgerChargesService:
        """Return custom ledger charges service."""
        return AsyncCustomLedgerChargesService(
            http_client=self.http_client,
            endpoint_params={"custom_ledger_id": custom_ledger_id},
        )

    def attachments(self, custom_ledger_id: str) -> AsyncCustomLedgerAttachmentsService:
        """Return custom ledger attachments service."""
        return AsyncCustomLedgerAttachmentsService(
            http_client=self.http_client,
            endpoint_params={"custom_ledger_id": custom_ledger_id},
        )
