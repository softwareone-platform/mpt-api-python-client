from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncGetMixin,
    AsyncUpdateMixin,
    GetMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model


class EventType(Model):
    """Event Type resource."""


class EventTypesServiceConfig:
    """Event Types service configuration."""

    _endpoint = "/public/v1/audit/event-types"
    _model_class = EventType
    _collection_key = "data"


class EventTypesService(
    UpdateMixin[EventType], GetMixin[EventType], Service[EventType], EventTypesServiceConfig
):
    """Event Types service."""


class AsyncEventTypesService(
    AsyncUpdateMixin[EventType],
    AsyncGetMixin[EventType],
    AsyncService[EventType],
    EventTypesServiceConfig,
):
    """Async Event Types service."""
