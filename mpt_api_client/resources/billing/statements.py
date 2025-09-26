from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import AsyncUpdateMixin, UpdateMixin
from mpt_api_client.models import Model
from mpt_api_client.resources.billing.mixins import AsyncIssuableMixin, IssuableMixin


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
    Service[Statement],
    StatementsServiceConfig,
):
    """Statements service."""


class AsyncStatementsService(
    AsyncUpdateMixin[Statement],
    AsyncIssuableMixin[Statement],
    AsyncService[Statement],
    StatementsServiceConfig,
):
    """Async Statements service."""
