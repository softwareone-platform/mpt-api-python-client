from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncUpdateMixin,
    CreateMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model


class ManualOverride(Model):
    """Manual Override resource."""


class ManualOverridesServiceConfig:
    """Manual Overrides service configuration."""

    _endpoint = "/public/v1/billing/manual-overrides"
    _model_class = ManualOverride
    _collection_key = "data"


class ManualOverridesService(
    CreateMixin[ManualOverride],
    UpdateMixin[ManualOverride],
    Service[ManualOverride],
    ManualOverridesServiceConfig,
):
    """Manual Overrides service."""


class AsyncManualOverridesService(
    AsyncCreateMixin[ManualOverride],
    AsyncUpdateMixin[ManualOverride],
    AsyncService[ManualOverride],
    ManualOverridesServiceConfig,
):
    """Async Manual Overrides service."""
