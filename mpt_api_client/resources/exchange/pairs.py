from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncGetMixin,
    CollectionMixin,
    GetMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class Pair(Model):
    """Exchange currency pair resource.

    Attributes:
        name: Pair name.
        external_id: External identifier of the pair.
        notes: Free-form notes for the pair.
        primary: Whether the pair is the primary one for its currencies.
        reverse: Reference to the pair holding the reverse conversion.
        source_currency: Currency converted from.
        destination_currency: Currency converted to.
        latest_rate: Most recent rate recorded for the pair.
        agreements: Number of agreements using the pair.
        rates: Number of rates recorded for the pair.
        status: Current status of the pair.
        revision: Revision number.
        audit: Audit information (created, updated events).
    """

    name: str | None
    external_id: str | None
    notes: str | None
    primary: bool | None
    reverse: BaseModel | None
    source_currency: BaseModel | None
    destination_currency: BaseModel | None
    latest_rate: BaseModel | None
    agreements: int | None
    rates: int | None
    status: str | None
    revision: int | None
    audit: BaseModel | None


class PairsServiceConfig:
    """Exchange Pairs service configuration."""

    _endpoint = "/public/v1/exchange/pairs"
    _model_class = Pair
    _collection_key = "data"


class PairsService(
    GetMixin[Pair],
    CollectionMixin[Pair],
    Service[Pair],
    PairsServiceConfig,
):
    """Exchange Pairs service."""


class AsyncPairsService(
    AsyncGetMixin[Pair],
    AsyncCollectionMixin[Pair],
    AsyncService[Pair],
    PairsServiceConfig,
):
    """Async Exchange Pairs service."""
