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
from mpt_api_client.resources.accounts.mixins import AsyncEnablableMixin, EnablableMixin


class ApiToken(Model):
    """API Token Model."""


class ApiTokensServiceConfig:
    """API Tokens Service Configuration."""

    _endpoint = "/public/v1/accounts/api-tokens"
    _model_class = ApiToken
    _collection_key = "data"


class ApiTokensService(
    CreateMixin[ApiToken],
    DeleteMixin,
    UpdateMixin[ApiToken],
    EnablableMixin[ApiToken],
    Service[ApiToken],
    ApiTokensServiceConfig,
):
    """API Tokens Service."""


class AsyncApiTokensService(
    AsyncCreateMixin[ApiToken],
    AsyncDeleteMixin,
    AsyncUpdateMixin[ApiToken],
    AsyncEnablableMixin[ApiToken],
    AsyncService[ApiToken],
    ApiTokensServiceConfig,
):
    """Async API Tokens Service."""
