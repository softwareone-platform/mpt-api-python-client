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


class CloudTenant(Model):
    """Cloud Tenant Model."""


class CloudTenantsServiceConfig:
    """Cloud Tenants Service Configuration."""

    _endpoint = "/public/v1/accounts/cloud-tenants"
    _model_class = CloudTenant
    _collection_key = "data"


class CloudTenantsService(
    CreateMixin[CloudTenant],
    DeleteMixin,
    UpdateMixin[CloudTenant],
    Service[CloudTenant],
    CloudTenantsServiceConfig,
):
    """Cloud Tenants Service."""


class AsyncCloudTenantsService(
    AsyncCreateMixin[CloudTenant],
    AsyncDeleteMixin,
    AsyncUpdateMixin[CloudTenant],
    AsyncService[CloudTenant],
    CloudTenantsServiceConfig,
):
    """Async Cloud Tenants Service."""
