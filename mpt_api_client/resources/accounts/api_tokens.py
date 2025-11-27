from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncDisableMixin,
    AsyncEnableMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    DisableMixin,
    EnableMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model


class ApiToken(Model):
    """API Token Model."""


class ApiTokensServiceConfig:
    """API Tokens Service Configuration."""

    _endpoint = "/public/v1/accounts/api-tokens"
    _model_class = ApiToken
    _collection_key = "data"


class ApiTokensService(
    ManagedResourceMixin[ApiToken],
    EnableMixin[ApiToken],
    DisableMixin[ApiToken],
    CollectionMixin[ApiToken],
    Service[ApiToken],
    ApiTokensServiceConfig,
):
    """API Tokens Service."""


class AsyncApiTokensService(
    AsyncManagedResourceMixin[ApiToken],
    AsyncEnableMixin[ApiToken],
    AsyncDisableMixin[ApiToken],
    AsyncCollectionMixin[ApiToken],
    AsyncService[ApiToken],
    ApiTokensServiceConfig,
):
    """Async API Tokens Service."""
