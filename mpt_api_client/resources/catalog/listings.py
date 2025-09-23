from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncUpdateMixin,
    CreateMixin,
    DeleteMixin,
    UpdateMixin,
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
    CreateMixin[Listing],
    DeleteMixin,
    UpdateMixin[Listing],
    Service[Listing],
    ListingsServiceConfig,
):
    """Listings service."""


class AsyncListingsService(
    AsyncCreateMixin[Listing],
    AsyncDeleteMixin,
    AsyncUpdateMixin[Listing],
    AsyncService[Listing],
    ListingsServiceConfig,
):
    """Listings service."""
