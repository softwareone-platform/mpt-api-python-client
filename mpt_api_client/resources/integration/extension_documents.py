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
from mpt_api_client.models import DocumentModel
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.mixins import AsyncPublishableMixin, PublishableMixin


class ExtensionDocument(DocumentModel):
    """Extension Document resource.

    Attributes:
        revision: Revision number.
        language: Language code.
        extension: Reference to the extension.
        audit: Audit information (created, updated, published, unpublished).
    """

    revision: int | None = None
    language: str | None = None
    extension: BaseModel | None = None
    audit: BaseModel | None = None


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
