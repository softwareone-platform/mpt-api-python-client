from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model


class OrderSubscription(Model):
    """Order Subscription resource."""


class OrderSubscriptionsServiceConfig:
    """Orders service config."""

    _endpoint = "/public/v1/commerce/orders/{order_id}/subscriptions"
    _model_class = OrderSubscription
    _collection_key = "data"


class OrderSubscriptionsService(  # noqa: WPS215
    ManagedResourceMixin[OrderSubscription],
    CollectionMixin[OrderSubscription],
    Service[OrderSubscription],
    OrderSubscriptionsServiceConfig,
):
    """Orders Subscription service."""


class AsyncOrderSubscriptionsService(  # noqa: WPS215
    AsyncManagedResourceMixin[OrderSubscription],
    AsyncCollectionMixin[OrderSubscription],
    AsyncService[OrderSubscription],
    OrderSubscriptionsServiceConfig,
):
    """Async Orders Subscription service."""
