from typing import override

from httpx._types import FileTypes

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncFilesOperationsMixin,
    AsyncModifiableResourceMixin,
    CollectionMixin,
    ModifiableResourceMixin,
)
from mpt_api_client.models import Model, ResourceData
from mpt_api_client.resources.catalog.mixins import (
    AsyncPublishableMixin,
    MediaMixin,
)


class Media(Model):
    """Media resource."""


class MediaServiceConfig:
    """Media service configuration."""

    _endpoint = "/public/v1/catalog/products/{product_id}/media"
    _model_class = Media
    _collection_key = "data"


class MediaService(
    MediaMixin[Media],
    ModifiableResourceMixin[Media],
    CollectionMixin[Media],
    Service[Media],
    MediaServiceConfig,
):
    """Media service."""


class AsyncMediaService(
    AsyncFilesOperationsMixin[Media],
    AsyncPublishableMixin[Media],
    AsyncModifiableResourceMixin[Media],
    AsyncCollectionMixin[Media],
    AsyncService[Media],
    MediaServiceConfig,
):
    """Media service."""

    @override
    async def create(
        self,
        resource_data: ResourceData | None = None,
        files: dict[str, FileTypes] | None = None,
        data_key: str = "_media_data",
    ) -> Media:
        """Create Media resource.

        Args:
            resource_data: Resource data.
            files: Files data.
            data_key: Key to use for the JSON data in the multipart form.

        Returns:
            Media resource.
        """
        return await super().create(resource_data=resource_data, files=files, data_key=data_key)
