from mpt_api_client.http import AsyncService, Service
from mpt_api_client.models import Model


class CustomLedgerCharge(Model):
    """Custom Ledger Charge resource."""


class CustomLedgerChargesServiceConfig:
    """Custom Ledger Charges service configuration."""

    _endpoint = "/public/v1/billing/custom-ledgers/{custom_ledger_id}/charges"
    _model_class = CustomLedgerCharge
    _collection_key = "data"


class CustomLedgerChargesService(
    Service[CustomLedgerCharge],
    CustomLedgerChargesServiceConfig,
):
    """Custom Ledger Charges service."""


class AsyncCustomLedgerChargesService(
    AsyncService[CustomLedgerCharge],
    CustomLedgerChargesServiceConfig,
):
    """Async Custom Ledger Charges service."""
