from mpt_api_client.http import AsyncService, Service
from mpt_api_client.models import Model


class StatementCharge(Model):
    """Statement Charge resource."""


class StatementChargesServiceConfig:
    """Statement Charges service configuration."""

    _endpoint = "/public/v1/billing/statements/{statement_id}/charges"
    _model_class = StatementCharge
    _collection_key = "data"


class StatementChargesService(
    Service[StatementCharge],
    StatementChargesServiceConfig,
):
    """Statement Charges service."""


class AsyncStatementChargesService(
    AsyncService[StatementCharge],
    StatementChargesServiceConfig,
):
    """Async Statement Charges service."""
