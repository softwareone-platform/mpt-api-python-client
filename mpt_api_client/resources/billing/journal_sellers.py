from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import AsyncGetMixin, GetMixin
from mpt_api_client.models import Model


class JournalSeller(Model):
    """Journal Seller resource."""


class JournalSellersServiceConfig:
    """Journal Sellers service configuration."""

    _endpoint = "/public/v1/billing/journals/{journal_id}/sellers"
    _model_class = JournalSeller
    _collection_key = "data"


class JournalSellersService(
    GetMixin[JournalSeller],
    Service[JournalSeller],
    JournalSellersServiceConfig,
):
    """Journal Sellers service."""


class AsyncJournalSellersService(
    AsyncGetMixin[JournalSeller],
    AsyncService[JournalSeller],
    JournalSellersServiceConfig,
):
    """Async Journal Sellers service."""
