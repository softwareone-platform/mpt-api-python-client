from mpt_api_client.http import (
    AsyncService,
    Service,
)
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateMixin,
    AsyncGetMixin,
    AsyncUpdateMixin,
    CollectionMixin,
    CreateMixin,
    GetMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.commerce.mixins import (
    AsyncRenderMixin,
    AsyncTerminateMixin,
    RenderMixin,
    TerminateMixin,
)


class Subscription(Model):
    """Subscription resource."""


class SubscriptionsServiceConfig:
    """Subscription service config."""

    _endpoint = "/public/v1/commerce/subscriptions"
    _model_class = Subscription
    _collection_key = "data"


class SubscriptionsService(  # noqa: WPS215
    CreateMixin[Subscription],
    UpdateMixin[Subscription],
    GetMixin[Subscription],
    CollectionMixin[Subscription],
    TerminateMixin[Subscription],
    RenderMixin[Subscription],
    Service[Subscription],
    SubscriptionsServiceConfig,
):
    """Subscription service."""


class AsyncSubscriptionsService(  # noqa: WPS215
    AsyncCreateMixin[Subscription],
    AsyncUpdateMixin[Subscription],
    AsyncGetMixin[Subscription],
    AsyncCollectionMixin[Subscription],
    AsyncTerminateMixin[Subscription],
    AsyncRenderMixin[Subscription],
    AsyncService[Subscription],
    SubscriptionsServiceConfig,
):
    """Async Subscription service."""
