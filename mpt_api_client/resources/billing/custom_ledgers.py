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
from mpt_api_client.resources.billing.mixins import AcceptableMixin, AsyncAcceptableMixin


class CustomLedger(Model):
    """Custom Ledger resource."""


class CustomLedgersServiceConfig:
    """Custom Ledgers service configuration."""

    _endpoint = "/public/v1/billing/custom-ledgers"
    _model_class = CustomLedger
    _collection_key = "data"


class CustomLedgersService(
    CreateMixin[CustomLedger],
    DeleteMixin,
    UpdateMixin[CustomLedger],
    AcceptableMixin[CustomLedger],
    Service[CustomLedger],
    CustomLedgersServiceConfig,
):
    """Custom Ledgers service."""


class AsyncCustomLedgersService(
    AsyncCreateMixin[CustomLedger],
    AsyncDeleteMixin,
    AsyncUpdateMixin[CustomLedger],
    AsyncAcceptableMixin[CustomLedger],
    AsyncService[CustomLedger],
    CustomLedgersServiceConfig,
):
    """Async Custom Ledgers service."""
