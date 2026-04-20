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
from mpt_api_client.resources.program.mixins import (
    AsyncPublishableMixin,
    PublishableMixin,
)


class TermVariant(Model):
    """Term variant resource.

    Attributes:
        name: The name of the term variant.
        type: The type of the term variant.
        asset_url: The URL of the asset.
        language_code: The language code of the term variant.
        description: The description of the term variant.
        status: The status of the term variant.
        filename: The filename of the term variant.
        size: The size of the term variant.
        content_type: The content type of the term variant.
        program_terms_and_conditions: The associated program terms and conditions.
        file_id: The ID of the file.
        audit: The audit information.
    """

    name: str | None
    type: str | None
    asset_url: str | None
    language_code: str | None
    description: str | None
    status: str | None
    filename: str | None
    size: int | None
    content_type: str | None
    program_terms_and_conditions: BaseModel | None
    file_id: str | None
    audit: BaseModel | None


class TermVariantServiceConfig:
    """Term variant service configuration."""

    _endpoint = "/public/v1/program/programs/{program_id}/terms/{term_id}/variants"
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
    """Async term variant service."""
