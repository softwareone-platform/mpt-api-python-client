from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncModifiableResourceMixin,
    CollectionMixin,
    ModifiableResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.catalog.mixins import (
    AsyncMediaMixin,
    MediaMixin,
)


class Media(Model):
    """Media resource."""


class MediaServiceConfig:
    """Media service configuration."""

    _endpoint = "/public/v1/catalog/products/{product_id}/media"
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
    """Media service."""
