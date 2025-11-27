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


class Subscriber(Model):
    """Subscriber resource."""


class SubscribersServiceConfig:
    """Subscribers service config."""

    _endpoint = "/public/v1/notifications/subscribers"
    _model_class = Subscriber
    _collection_key = "data"


class SubscribersService(
    EnableMixin[Subscriber],
    DisableMixin[Subscriber],
    ManagedResourceMixin[Subscriber],
    CollectionMixin[Subscriber],
    Service[Subscriber],
    SubscribersServiceConfig,
):
    """Subscribers service."""


class AsyncSubscribersService(
    AsyncEnableMixin[Subscriber],
    AsyncDisableMixin[Subscriber],
    AsyncManagedResourceMixin[Subscriber],
    AsyncCollectionMixin[Subscriber],
    AsyncService[Subscriber],
    SubscribersServiceConfig,
):
    """Async Subscribers service."""
