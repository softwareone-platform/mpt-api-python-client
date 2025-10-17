from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model


class Listing(Model):
    """Listing resource."""


class ListingsServiceConfig:
    """Listings service configuration."""

    _endpoint = "/public/v1/catalog/listings"
    _model_class = Listing
    _collection_key = "data"


class ListingsService(
    ManagedResourceMixin[Listing],
    CollectionMixin[Listing],
    Service[Listing],
    ListingsServiceConfig,
):
    """Listings service."""


class AsyncListingsService(
    AsyncManagedResourceMixin[Listing],
    AsyncCollectionMixin[Listing],
    AsyncService[Listing],
    ListingsServiceConfig,
):
    """Listings service."""
