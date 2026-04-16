from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncModifiableResourceMixin,
    CollectionMixin,
    ModifiableResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.program.mixins import (
    AsyncMediaMixin,
    MediaMixin,
)


class Media(Model):
    """Media resource.

    Attributes:
        name: Media name.
        type: Media type.
        description: Media description.
        status: Media status.
        filename: Original file name.
        size: File size in bytes.
        content_type: MIME content type of the media file.
        display_order: Display order of the media item.
        url: URL to access the media file.
        program: Reference to the program.
        audit: Audit information (created, updated events).
    """

    name: str | None
    type: str | None
    description: str | None
    status: str | None
    filename: str | None
    size: int | None
    content_type: str | None
    display_order: int | None
    url: str | None
    program: BaseModel | None
    audit: BaseModel | None


class MediaServiceConfig:
    """Media service configuration."""

    _endpoint = "/public/v1/program/programs/{program_id}/media"
    _model_class = Media
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "media"


class MediaService(
    MediaMixin[Media],
    ModifiableResourceMixin[Media],
    CollectionMixin[Media],
    Service[Media],
    MediaServiceConfig,
):
    """Media service."""


class AsyncMediaService(
    AsyncMediaMixin[Media],
    AsyncModifiableResourceMixin[Media],
    AsyncCollectionMixin[Media],
    AsyncService[Media],
    MediaServiceConfig,
):
    """Async media service."""
