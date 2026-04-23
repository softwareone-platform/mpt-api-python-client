from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateFileMixin,
    AsyncDownloadFileMixin,
    AsyncModifiableResourceMixin,
    CollectionMixin,
    CreateFileMixin,
    DownloadFileMixin,
    ModifiableResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.mixins import AsyncPublishableMixin, PublishableMixin


class ExtensionDocument(Model):
    """Extension Document resource.

    Attributes:
        name: Document name.
        revision: Revision number.
        type: Document type (Online or File).
        description: Document description.
        status: Document status (Draft, Published, Unpublished, Deleted).
        filename: Original file name.
        size: File size in bytes.
        content_type: MIME content type.
        url: URL to access the document.
        language: Language code.
        extension: Reference to the extension.
        audit: Audit information (created, updated, published, unpublished).
    """

    name: str | None
    revision: int | None
    type: str | None
    description: str | None
    status: str | None
    filename: str | None
    size: int | None
    content_type: str | None
    url: str | None
    language: str | None
    extension: BaseModel | None
    audit: BaseModel | None


class ExtensionDocumentsServiceConfig:
    """Extension Documents service configuration."""

    _endpoint = "/public/v1/integration/extensions/{extension_id}/documents"
    _model_class = ExtensionDocument
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "document"


class ExtensionDocumentsService(
    PublishableMixin[ExtensionDocument],
    DownloadFileMixin[ExtensionDocument],
    CreateFileMixin[ExtensionDocument],
    ModifiableResourceMixin[ExtensionDocument],
    CollectionMixin[ExtensionDocument],
    Service[ExtensionDocument],
    ExtensionDocumentsServiceConfig,
):
    """Sync service for /public/v1/integration/extensions/{extensionId}/documents endpoint."""


class AsyncExtensionDocumentsService(
    AsyncPublishableMixin[ExtensionDocument],
    AsyncDownloadFileMixin[ExtensionDocument],
    AsyncCreateFileMixin[ExtensionDocument],
    AsyncModifiableResourceMixin[ExtensionDocument],
    AsyncCollectionMixin[ExtensionDocument],
    AsyncService[ExtensionDocument],
    ExtensionDocumentsServiceConfig,
):
    """Async service for /public/v1/integration/extensions/{extensionId}/documents endpoint."""
