from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.mixins import AsyncPublishableMixin, PublishableMixin
from mpt_api_client.resources.program.programs_terms_variant import (
    AsyncTermVariantService,
    TermVariantService,
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

    def variants(self, term_id: str) -> TermVariantService:
        """Access program term variants service."""
        return TermVariantService(
            http_client=self.http_client,
            endpoint_params={"program_id": self.endpoint_params["program_id"], "term_id": term_id},
        )


class AsyncTermService(
    AsyncPublishableMixin[Term],
    AsyncManagedResourceMixin[Term],
    AsyncCollectionMixin[Term],
    AsyncService[Term],
    TermServiceConfig,
):
    """Async program term service."""

    def variants(self, term_id: str) -> AsyncTermVariantService:
        """Access async program term variants service."""
        return AsyncTermVariantService(
            http_client=self.http_client,
            endpoint_params={"program_id": self.endpoint_params["program_id"], "term_id": term_id},
        )
