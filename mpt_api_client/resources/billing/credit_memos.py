from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncUpdateMixin,
    CreateMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.billing.credit_memo_attachments import (
    AsyncCreditMemoAttachmentsService,
    CreditMemoAttachmentsService,
)


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

    def attachments(self, credit_memo_id: str) -> CreditMemoAttachmentsService:
        """Return credit memo attachments service."""
        return CreditMemoAttachmentsService(
            http_client=self.http_client,
            endpoint_params={"credit_memo_id": credit_memo_id},
        )


class AsyncCreditMemosService(
    AsyncCreateMixin[CreditMemo],
    AsyncUpdateMixin[CreditMemo],
    AsyncService[CreditMemo],
    CreditMemosServiceConfig,
):
    """Async Credit Memos service."""

    def attachments(self, credit_memo_id: str) -> AsyncCreditMemoAttachmentsService:
        """Return credit memo attachments service."""
        return AsyncCreditMemoAttachmentsService(
            http_client=self.http_client,
            endpoint_params={"credit_memo_id": credit_memo_id},
        )
