from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.accounts.mixins import AsyncEnablableMixin, EnablableMixin


class ApiToken(Model):
    """API Token Model."""


class ApiTokensServiceConfig:
    """API Tokens Service Configuration."""

    _endpoint = "/public/v1/accounts/api-tokens"
    _model_class = ApiToken
    _collection_key = "data"


class ApiTokensService(
    ManagedResourceMixin[ApiToken],
    EnablableMixin[ApiToken],
    CollectionMixin[ApiToken],
    Service[ApiToken],
    ApiTokensServiceConfig,
):
    """API Tokens Service."""


class AsyncApiTokensService(
    AsyncManagedResourceMixin[ApiToken],
    AsyncEnablableMixin[ApiToken],
    AsyncCollectionMixin[ApiToken],
    AsyncService[ApiToken],
    ApiTokensServiceConfig,
):
    """Async API Tokens Service."""
