from mpt_api_client.http import (
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncService,
    AsyncUpdateMixin,
    CreateMixin,
    DeleteMixin,
    Service,
    UpdateMixin,
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
    CreateMixin[OrderSubscription],
    DeleteMixin,
    UpdateMixin[OrderSubscription],
    Service[OrderSubscription],
    OrderSubscriptionsServiceConfig,
):
    """Orders Subscription service."""


class AsyncOrderSubscriptionsService(  # noqa: WPS215
    AsyncCreateMixin[OrderSubscription],
    AsyncDeleteMixin,
    AsyncUpdateMixin[OrderSubscription],
    AsyncService[OrderSubscription],
    OrderSubscriptionsServiceConfig,
):
    """Async Orders Subscription service."""
