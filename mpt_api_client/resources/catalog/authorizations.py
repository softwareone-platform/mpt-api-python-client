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


class Authorization(Model):
    """Authorization resource."""


class AuthorizationsServiceConfig:
    """Authorizations service configuration."""

    _endpoint = "/public/v1/catalog/authorizations"
    _model_class = Authorization
    _collection_key = "data"


class AuthorizationsService(
    CreateMixin[Authorization],
    DeleteMixin,
    GetMixin[Authorization],
    UpdateMixin[Authorization],
    Service[Authorization],
    AuthorizationsServiceConfig,
):
    """Authorizations service."""


class AsyncAuthorizationsService(
    AsyncCreateMixin[Authorization],
    AsyncDeleteMixin,
    AsyncGetMixin[Authorization],
    AsyncUpdateMixin[Authorization],
    AsyncService[Authorization],
    AuthorizationsServiceConfig,
):
    """Authorizations service."""
