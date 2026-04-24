from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncGetMixin,
    CollectionMixin,
    GetMixin,
)
from mpt_api_client.models import Model


class SpotlightQuery(Model):
    """Spotlight Query resource.

    Attributes:
        id: Unique identifier for the spotlight query.
        name: Name of the spotlight query.
        template: Template string for the spotlight query.
        invalidation_interval: Interval for invalidating the spotlight query.
        invalidate_on_date_change: Whether to invalidate the spotlight query on date change.
        filter: Filter string for the spotlight query.
        scope: Scope of the spotlight query.
    """

    id: str = ""
    name: str | None
    template: str | None
    invalidation_interval: str | None
    invalidate_on_date_change: bool | None
    filter: str | None
    scope: str | None


class SpotlightQueriesServiceConfig:
    """Configuration for Spotlight Queries Service."""

    _endpoint: str = "/public/v1/spotlight/queries"
    _model_class = SpotlightQuery
    _collection_key = "data"


class SpotlightQueriesService(
    GetMixin[SpotlightQuery],
    CollectionMixin[SpotlightQuery],
    Service[SpotlightQuery],
    SpotlightQueriesServiceConfig,
):
    """Service for spotlight queries."""


class AsyncSpotlightQueriesService(
    AsyncGetMixin[SpotlightQuery],
    AsyncCollectionMixin[SpotlightQuery],
    AsyncService[SpotlightQuery],
    SpotlightQueriesServiceConfig,
):
    """Asynchronous service for spotlight queries."""
