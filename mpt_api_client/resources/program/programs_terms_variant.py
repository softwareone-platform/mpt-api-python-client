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
from mpt_api_client.resources.mixins import AsyncPublishableMixin, PublishableMixin


class TermVariant(TermVariantModel):
    """Term variant resource.

    Attributes:
        program_terms_and_conditions: The associated program terms and conditions.
        audit: The audit information.
    """

    program_terms_and_conditions: BaseModel | None = None
    audit: BaseModel | None = None


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
