from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncGetMixin,
    AsyncUpdateMixin,
    CollectionMixin,
    GetMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.billing.mixins import AsyncIssuableMixin, IssuableMixin
from mpt_api_client.resources.billing.statement_attachments import (
    AsyncStatementAttachmentsService,
    StatementAttachmentsService,
)
from mpt_api_client.resources.billing.statement_charges import (
    AsyncStatementChargesService,
    StatementChargesService,
)


class Statement(Model):
    """Statement resource."""


class StatementsServiceConfig:
    """Statements service configuration."""

    _endpoint = "/public/v1/billing/statements"
    _model_class = Statement
    _collection_key = "data"


class StatementsService(
    UpdateMixin[Statement],
    IssuableMixin[Statement],
    GetMixin[Statement],
    CollectionMixin[Statement],
    Service[Statement],
    StatementsServiceConfig,
):
    """Statements service."""

    def charges(self, statement_id: str) -> StatementChargesService:
        """Return statement charges service."""
        return StatementChargesService(
            http_client=self.http_client,
            endpoint_params={"statement_id": statement_id},
        )

    def attachments(self, statement_id: str) -> StatementAttachmentsService:
        """Return statement attachments service."""
        return StatementAttachmentsService(
            http_client=self.http_client,
            endpoint_params={"statement_id": statement_id},
        )


class AsyncStatementsService(
    AsyncUpdateMixin[Statement],
    AsyncIssuableMixin[Statement],
    AsyncGetMixin[Statement],
    AsyncCollectionMixin[Statement],
    AsyncService[Statement],
    StatementsServiceConfig,
):
    """Async Statements service."""

    def charges(self, statement_id: str) -> AsyncStatementChargesService:
        """Return statement charges service."""
        return AsyncStatementChargesService(
            http_client=self.http_client,
            endpoint_params={"statement_id": statement_id},
        )

    def attachments(self, statement_id: str) -> AsyncStatementAttachmentsService:
        """Return statement attachments service."""
        return AsyncStatementAttachmentsService(
            http_client=self.http_client,
            endpoint_params={"statement_id": statement_id},
        )
