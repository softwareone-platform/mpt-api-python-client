from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import AsyncGetMixin, AsyncUpdateMixin, GetMixin, UpdateMixin
from mpt_api_client.models import Model
from mpt_api_client.resources.billing.mixins import AsyncIssuableMixin, IssuableMixin
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


class AsyncStatementsService(
    AsyncUpdateMixin[Statement],
    AsyncIssuableMixin[Statement],
    AsyncGetMixin[Statement],
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
