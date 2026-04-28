from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncModifiableResourceMixin,
    CollectionMixin,
    ModifiableResourceMixin,
)
from mpt_api_client.models import MediaModel
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.mixins import (
    AsyncMediaMixin,
    AsyncReviewableMixin,
    MediaMixin,
    ReviewableMixin,
)


class Media(MediaModel):
    """Media resource.

    Attributes:
        product: Reference to the product.
        audit: Audit information (created, updated events).
    """

    product: BaseModel | None = None
    audit: BaseModel | None = None


class MediaServiceConfig:
    """Media service configuration."""

    _endpoint = "/public/v1/catalog/products/{product_id}/media"
    _model_class = Media
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "media"


class MediaService(
    MediaMixin[Media],
    ReviewableMixin[Media],
    ModifiableResourceMixin[Media],
    CollectionMixin[Media],
    Service[Media],
    MediaServiceConfig,
):
    """Media service."""


class AsyncMediaService(
    AsyncMediaMixin[Media],
    AsyncReviewableMixin[Media],
    AsyncModifiableResourceMixin[Media],
    AsyncCollectionMixin[Media],
    AsyncService[Media],
    MediaServiceConfig,
):
    """Media service."""
