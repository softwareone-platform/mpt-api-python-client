from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateFileMixin,
    AsyncDeleteMixin,
    AsyncDownloadFileMixin,
    AsyncModifiableResourceMixin,
    CollectionMixin,
    CreateFileMixin,
    DeleteMixin,
    DownloadFileMixin,
    ModifiableResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.integration.mixins import (
    AsyncMediaMixin,
    AsyncPublishableMixin,
    MediaMixin,
    PublishableMixin,
)


class ExtensionMedia(Model):
    """Extension Media resource.

    Attributes:
        name: Media name.
        revision: Revision number.
        type: Media type (Video or Image).
        description: Media description.
        status: Media status (Draft, Published, Unpublished, Deleted).
        filename: Original file name.
        size: File size in bytes.
        content_type: MIME content type.
        display_order: Display order.
        url: URL to access the media.
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
    display_order: int | None
    url: str | None
    extension: BaseModel | None
    audit: BaseModel | None


class ExtensionMediaServiceConfig:
    """Extension Media service configuration."""

    _endpoint = "/public/v1/integration/extensions/{extension_id}/media"
    _model_class = ExtensionMedia
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "media"


class ExtensionMediaService(
    MediaMixin[ExtensionMedia],
    PublishableMixin[ExtensionMedia],
    DownloadFileMixin[ExtensionMedia],
    CreateFileMixin[ExtensionMedia],
    ModifiableResourceMixin[ExtensionMedia],
    DeleteMixin,
    CollectionMixin[ExtensionMedia],
    Service[ExtensionMedia],
    ExtensionMediaServiceConfig,
):
    """Sync service for the /public/v1/integration/extensions/{extensionId}/media endpoint."""


class AsyncExtensionMediaService(
    AsyncMediaMixin[ExtensionMedia],
    AsyncPublishableMixin[ExtensionMedia],
    AsyncDownloadFileMixin[ExtensionMedia],
    AsyncCreateFileMixin[ExtensionMedia],
    AsyncModifiableResourceMixin[ExtensionMedia],
    AsyncDeleteMixin,
    AsyncCollectionMixin[ExtensionMedia],
    AsyncService[ExtensionMedia],
    ExtensionMediaServiceConfig,
):
    """Async service for the /public/v1/integration/extensions/{extensionId}/media endpoint."""
