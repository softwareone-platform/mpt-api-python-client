from mpt_api_client.http import AsyncService, CreateMixin, DeleteMixin, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncUpdateMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.catalog.mixins import AsyncPublishableMixin, PublishableMixin


class Term(Model):
    """Term resource."""


class TermServiceConfig:
    """Term service configuration."""

    _endpoint = "/public/v1/catalog/products/{product_id}/terms"
    _model_class = Term
    _collection_key = "data"


class TermService(
    CreateMixin[Term],
    DeleteMixin,
    UpdateMixin[Term],
    PublishableMixin[Term],
    Service[Term],
    TermServiceConfig,
):
    """Term service."""


class AsyncTermService(
    AsyncCreateMixin[Term],
    AsyncDeleteMixin,
    AsyncUpdateMixin[Term],
    AsyncPublishableMixin[Term],
    AsyncService[Term],
    TermServiceConfig,
):
    """Async Term service."""
