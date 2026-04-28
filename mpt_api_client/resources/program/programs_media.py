from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncModifiableResourceMixin,
    CollectionMixin,
    ModifiableResourceMixin,
)
from mpt_api_client.models import MediaModel
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.mixins import AsyncMediaMixin, MediaMixin


class Media(MediaModel):
    """Media resource.

    Attributes:
        program: Reference to the program.
        audit: Audit information (created, updated events).
    """

    program: BaseModel | None = None
    audit: BaseModel | None = None


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
