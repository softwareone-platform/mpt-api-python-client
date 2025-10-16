from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncGetMixin,
    AsyncUpdateMixin,
    CreateMixin,
    DeleteMixin,
    GetMixin,
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
    GetMixin[Listing],
    UpdateMixin[Listing],
    Service[Listing],
    ListingsServiceConfig,
):
    """Listings service."""


class AsyncListingsService(
    AsyncCreateMixin[Listing],
    AsyncDeleteMixin,
    AsyncGetMixin[Listing],
    AsyncUpdateMixin[Listing],
    AsyncService[Listing],
    ListingsServiceConfig,
):
    """Listings service."""
