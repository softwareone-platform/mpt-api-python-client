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
from mpt_api_client.models import TermVariantModel
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.mixins import (
    AsyncPublishableMixin,
    AsyncReviewableMixin,
    PublishableMixin,
    ReviewableMixin,
)


class TermVariant(TermVariantModel):
    """Term variant resource.

    Attributes:
        terms_and_conditions: Reference to the parent terms and conditions.
        audit: Audit information (created, updated events).
    """

    terms_and_conditions: BaseModel | None = None
    audit: BaseModel | None = None


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
    ReviewableMixin[TermVariant],
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
    AsyncReviewableMixin[TermVariant],
    AsyncCollectionMixin[TermVariant],
    AsyncService[TermVariant],
    TermVariantServiceConfig,
):
    """Async Term variant service."""
