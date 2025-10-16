from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import AsyncGetMixin, GetMixin
from mpt_api_client.models import Model


class LedgerCharge(Model):
    """Ledger Charge resource."""


class LedgerChargesServiceConfig:
    """Ledger Charges service configuration."""

    _endpoint = "/public/v1/billing/ledgers/{ledger_id}/charges"
    _model_class = LedgerCharge
    _collection_key = "data"


class LedgerChargesService(
    GetMixin[LedgerCharge],
    Service[LedgerCharge],
    LedgerChargesServiceConfig,
):
    """Ledger Charges service."""


class AsyncLedgerChargesService(
    AsyncGetMixin[LedgerCharge],
    AsyncService[LedgerCharge],
    LedgerChargesServiceConfig,
):
    """Async Ledger Charges service."""
