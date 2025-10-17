from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model


class Authorization(Model):
    """Authorization resource."""


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
