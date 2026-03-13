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
from mpt_api_client.resources.catalog.mixins import (
    AsyncPublishableMixin,
    PublishableMixin,
)


class TermVariant(Model):
    """Term variant resource.

    Attributes:
        type: Variant type.
        asset_url: URL to the term variant asset.
        language_code: Language code for this variant.
        name: Variant name.
        description: Variant description.
        status: Variant status.
        filename: Original file name.
        size: File size in bytes.
        content_type: MIME content type of the file.
        terms_and_conditions: Reference to the parent terms and conditions.
        file_id: Identifier of the uploaded file.
        audit: Audit information (created, updated events).
    """

    type: str | None
    asset_url: str | None
    language_code: str | None
    name: str | None
    description: str | None
    status: str | None
    filename: str | None
    size: int | None
    content_type: str | None
    terms_and_conditions: BaseModel | None
    file_id: str | None
    audit: BaseModel | None


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
