from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class Listing(Model):
    """Listing resource.

    Attributes:
        authorization: Reference to the authorization.
        product: Reference to the product.
        vendor: Reference to the vendor.
        seller: Reference to the seller.
        price_list: Reference to the associated price list.
        primary: Whether this is the primary listing.
        notes: Additional notes.
        statistics: Listing statistics.
        eligibility: Eligibility information.
        audit: Audit information (created, updated events).
    """

    authorization: BaseModel | None
    product: BaseModel | None
    vendor: BaseModel | None
    seller: BaseModel | None
    price_list: BaseModel | None
    primary: bool | None
    notes: str | None
    statistics: BaseModel | None
    eligibility: BaseModel | None
    audit: BaseModel | None


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
