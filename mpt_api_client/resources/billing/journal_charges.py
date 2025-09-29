from mpt_api_client.http import AsyncService, Service
from mpt_api_client.models import Model


class JournalCharge(Model):
    """Journal Charge resource."""


class JournalChargesServiceConfig:
    """Journal Charges service configuration."""

    _endpoint = "/public/v1/billing/journals/{journal_id}/charges"
    _model_class = JournalCharge
    _collection_key = "data"


class JournalChargesService(
    Service[JournalCharge],
    JournalChargesServiceConfig,
):
    """Journal Charges service."""


class AsyncJournalChargesService(
    AsyncService[JournalCharge],
    JournalChargesServiceConfig,
):
    """Async Journal Charges service."""
