from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncDownloadFileMixin,
    AsyncModifiableResourceMixin,
    CollectionMixin,
    DownloadFileMixin,
    ModifiableResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.catalog.mixins import (
    AsyncCreateFileMixin,
    AsyncPublishableMixin,
    CreateFileMixin,
    PublishableMixin,
)


class TermVariant(Model):
    """Term variant resource."""


class TermVariantServiceConfig:
    """Term variant service configuration."""

    _endpoint = "/public/v1/catalog/products/{product_id}/terms/{term_id}/variants"
    _model_class = TermVariant
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "variant"


class TermVariantService(
    CreateFileMixin[TermVariant],
    DownloadFileMixin[TermVariant],
    ModifiableResourceMixin[TermVariant],
    PublishableMixin[TermVariant],
    CollectionMixin[TermVariant],
    Service[TermVariant],
    TermVariantServiceConfig,
):
    """Term variant service."""


class AsyncTermVariantService(
    AsyncCreateFileMixin[TermVariant],
    AsyncDownloadFileMixin[TermVariant],
    AsyncModifiableResourceMixin[TermVariant],
    AsyncPublishableMixin[TermVariant],
    AsyncCollectionMixin[TermVariant],
    AsyncService[TermVariant],
    TermVariantServiceConfig,
):
    """Async Term variant service."""
