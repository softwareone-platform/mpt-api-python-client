from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateMixin,
    AsyncGetMixin,
    AsyncUpdateMixin,
    CollectionMixin,
    CreateMixin,
    GetMixin,
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
    GetMixin[CreditMemo],
    CollectionMixin[CreditMemo],
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
    AsyncGetMixin[CreditMemo],
    AsyncCollectionMixin[CreditMemo],
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
