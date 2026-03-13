from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class Authorization(Model):
    """Authorization resource.

    Attributes:
        name: Authorization name.
        external_ids: External identifiers for the authorization.
        currency: Currency code associated with the authorization.
        notes: Additional notes.
        product: Reference to the product.
        vendor: Reference to the vendor.
        owner: Reference to the owner account.
        statistics: Authorization statistics.
        journal: Journal reference.
        eligibility: Eligibility information.
        audit: Audit information (created, updated events).
    """

    name: str | None
    external_ids: BaseModel | None
    currency: str | None
    notes: str | None
    product: BaseModel | None
    vendor: BaseModel | None
    owner: BaseModel | None
    statistics: BaseModel | None
    journal: BaseModel | None
    eligibility: BaseModel | None
    audit: BaseModel | None


class AuthorizationsServiceConfig:
    """Authorizations service configuration."""

    _endpoint = "/public/v1/catalog/authorizations"
    _model_class = Authorization
    _collection_key = "data"


class AuthorizationsService(
    ManagedResourceMixin[Authorization],
    CollectionMixin[Authorization],
    Service[Authorization],
    AuthorizationsServiceConfig,
):
    """Authorizations service."""


class AsyncAuthorizationsService(
    AsyncManagedResourceMixin[Authorization],
    AsyncCollectionMixin[Authorization],
    AsyncService[Authorization],
    AuthorizationsServiceConfig,
):
    """Authorizations service."""
