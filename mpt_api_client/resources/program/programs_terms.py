from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.program.mixins import (
    AsyncPublishableMixin,
    PublishableMixin,
)


class Term(Model):
    """Program term resource.

    Attributes:
         name: Program term name.
         description: Program term description.
         display_order: Display order of the program term.
         status: Program term status.
         program: Reference to the program.
         audit: Audit information (created, updated events).
    """

    name: str | None
    description: str | None
    display_order: int | None
    status: str | None
    program: BaseModel | None
    audit: BaseModel | None


class TermServiceConfig:
    """Program term service configuration."""

    _endpoint = "/public/v1/program/programs/{program_id}/terms"
    _model_class = Term
    _collection_key = "data"


class TermService(
    PublishableMixin[Term],
    ManagedResourceMixin[Term],
    CollectionMixin[Term],
    Service[Term],
    TermServiceConfig,
):
    """Program term service."""


class AsyncTermService(
    AsyncPublishableMixin[Term],
    AsyncManagedResourceMixin[Term],
    AsyncCollectionMixin[Term],
    AsyncService[Term],
    TermServiceConfig,
):
    """Async program term service."""
