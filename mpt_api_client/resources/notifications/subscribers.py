from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model


class Subscriber(Model):
    """Subscriber resource."""


class SubscribersServiceConfig:
    """Subscribers service config."""

    _endpoint = "/public/v1/notifications/subscribers"
    _model_class = Subscriber
    _collection_key = "data"


class SubscribersService(
    ManagedResourceMixin[Subscriber],
    CollectionMixin[Subscriber],
    Service[Subscriber],
    SubscribersServiceConfig,
):
    """Subscribers service."""


class AsyncSubscribersService(
    AsyncManagedResourceMixin[Subscriber],
    AsyncCollectionMixin[Subscriber],
    AsyncService[Subscriber],
    SubscribersServiceConfig,
):
    """Async Subscribers service."""
