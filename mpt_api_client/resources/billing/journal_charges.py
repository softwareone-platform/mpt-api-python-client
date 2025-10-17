from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncGetMixin,
    CollectionMixin,
    GetMixin,
)
from mpt_api_client.models import Model


class JournalCharge(Model):
    """Journal Charge resource."""


class JournalChargesServiceConfig:
    """Journal Charges service configuration."""

    _endpoint = "/public/v1/billing/journals/{journal_id}/charges"
    _model_class = JournalCharge
    _collection_key = "data"


class JournalChargesService(
    GetMixin[JournalCharge],
    CollectionMixin[JournalCharge],
    Service[JournalCharge],
    JournalChargesServiceConfig,
):
    """Journal Charges service."""


class AsyncJournalChargesService(
    AsyncGetMixin[JournalCharge],
    AsyncCollectionMixin[JournalCharge],
    AsyncService[JournalCharge],
    JournalChargesServiceConfig,
):
    """Async Journal Charges service."""
