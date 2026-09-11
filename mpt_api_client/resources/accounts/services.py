from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncGetMixin,
    CollectionMixin,
    GetMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class ServiceIdentity(Model):
    """Service identity resource exposed by the accounts services endpoint.

    Attributes:
        name: Service identity name.
        status: Service identity status.
        description: Service identity description.
        icon: URL or identifier for the service identity icon.
        audit: Audit information.
    """

    name: str | None
    status: str | None
    description: str | None
    icon: str | None
    audit: BaseModel | None


class ServicesServiceConfig:
    """Services Service Configuration."""

    _endpoint = "/public/v1/accounts/services"
    _model_class = ServiceIdentity
    _collection_key = "data"


class ServicesService(
    GetMixin[ServiceIdentity],
    CollectionMixin[ServiceIdentity],
    Service[ServiceIdentity],
    ServicesServiceConfig,
):
    """Services Service."""


class AsyncServicesService(
    AsyncGetMixin[ServiceIdentity],
    AsyncCollectionMixin[ServiceIdentity],
    AsyncService[ServiceIdentity],
    ServicesServiceConfig,
):
    """Asynchronous Services Service."""
