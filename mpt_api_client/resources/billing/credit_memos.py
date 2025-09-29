from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncUpdateMixin,
    CreateMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model


class CreditMemo(Model):
    """Credit Memo resource."""


class CreditMemosServiceConfig:
    """Credit Memos service configuration."""

    _endpoint = "/public/v1/billing/credit-memos"
    _model_class = CreditMemo
    _collection_key = "data"


class CreditMemosService(
    CreateMixin[CreditMemo],
    UpdateMixin[CreditMemo],
    Service[CreditMemo],
    CreditMemosServiceConfig,
):
    """Credit Memos service."""


class AsyncCreditMemosService(
    AsyncCreateMixin[CreditMemo],
    AsyncUpdateMixin[CreditMemo],
    AsyncService[CreditMemo],
    CreditMemosServiceConfig,
):
    """Async Credit Memos service."""
