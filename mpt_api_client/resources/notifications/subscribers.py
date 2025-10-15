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


class Subscriber(Model):
    """Subscriber resource."""


class SubscribersServiceConfig:
    """Subscribers service config."""

    _endpoint = "/public/v1/notifications/subscribers"
    _model_class = Subscriber
    _collection_key = "data"


class SubscribersService(  # noqa: WPS215
    CreateMixin[Subscriber],
    UpdateMixin[Subscriber],
    GetMixin[Subscriber],
    DeleteMixin,
    Service[Subscriber],
    SubscribersServiceConfig,
):
    """Subscribers service."""


class AsyncSubscribersService(  # noqa: WPS215
    AsyncCreateMixin[Subscriber],
    AsyncUpdateMixin[Subscriber],
    AsyncGetMixin[Subscriber],
    AsyncDeleteMixin,
    AsyncService[Subscriber],
    SubscribersServiceConfig,
):
    """Async Subscribers service."""
