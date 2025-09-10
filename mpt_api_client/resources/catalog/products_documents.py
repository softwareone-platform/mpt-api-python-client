import json
from typing import override

from httpx import Response
from httpx._types import FileTypes

from mpt_api_client.http import AsyncService, CreateMixin, DeleteMixin, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncUpdateMixin,
    UpdateMixin,
)
from mpt_api_client.models import FileModel, Model, ResourceData
from mpt_api_client.resources.catalog.mixins import AsyncPublishableMixin, PublishableMixin


def _json_to_file_payload(resource_data: ResourceData) -> bytes:
    return json.dumps(
        resource_data, ensure_ascii=False, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


class Document(Model):
    """Document resource."""


class DocumentServiceConfig:
    """Document service configuration."""

    _endpoint = "/public/v1/catalog/products/{product_id}/documents"
    _model_class = Document
    _collection_key = "data"


class DocumentService(
    CreateMixin[Document],
    DeleteMixin,
    UpdateMixin[Document],
    PublishableMixin[Document],
    Service[Document],
    DocumentServiceConfig,
):
    """Document service."""

    @override
    def create(
        self,
        resource_data: ResourceData | None = None,
        files: dict[str, FileTypes] | None = None,  # noqa: WPS221
    ) -> Document:
        """Create Document resource.

        Include the document as a file or add an url in resource_data to be uploaded.

        Args:
            resource_data: Resource data.
            files: Files data.

        Returns:
            Document resource.
        """
        files = files or {}

        if resource_data:
            files["_attachment_data"] = (
                None,
                _json_to_file_payload(resource_data),
                "application/json",
            )

        response = self.http_client.post(self.endpoint, files=files)
        response.raise_for_status()
        return Document.from_response(response)

    def download(self, document_id: str) -> FileModel:
        """Download the document file for the given document ID.

        Args:
            document_id: Document ID.

        Returns:
            Document file.
        """
        response: Response = self._resource_do_request(
            document_id, method="GET", headers={"Accept": "*"}
        )
        return FileModel(response)


class AsyncDocumentService(
    AsyncCreateMixin[Document],
    AsyncDeleteMixin,
    AsyncUpdateMixin[Document],
    AsyncPublishableMixin[Document],
    AsyncService[Document],
    DocumentServiceConfig,
):
    """Document service."""

    @override
    async def create(
        self,
        resource_data: ResourceData | None = None,
        files: dict[str, FileTypes] | None = None,  # noqa: WPS221
    ) -> Document:
        """Create Document resource.

        Include the document as a file or add an url in resource_data to be uploaded.

        Args:
            resource_data: Resource data.
            files: Files data.

        Returns:
            Document resource.
        """
        files = files or {}

        if resource_data:
            files["_attachment_data"] = (
                None,
                _json_to_file_payload(resource_data),
                "application/json",
            )

        response = await self.http_client.post(self.endpoint, files=files)
        response.raise_for_status()
        return Document.from_response(response)

    async def download(self, document_id: str) -> FileModel:
        """Download the document file for the given document ID.

        Args:
            document_id: Document ID.

        Returns:
            Document file.
        """
        response = await self._resource_do_request(
            document_id, method="GET", headers={"Accept": "*"}
        )
        return FileModel(response)
