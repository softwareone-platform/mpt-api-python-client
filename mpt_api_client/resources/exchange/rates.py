from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncGetMixin,
    AsyncUpdateMixin,
    CollectionMixin,
    CreateMixin,
    DeleteMixin,
    GetMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class Rate(Model):
    """Exchange rate resource.

    Attributes:
        pair: Reference to the currency pair this rate applies to.
        external_id: Identifier of the external system the rate was fetched from.
        record_date: Date and time when this rate was fetched.
        value: The exchange rate from the pair's source currency to its destination currency.
            Serialized as a JSON number, sometimes in exponent form (``3.861e-05``), so callers
            converting it to Decimal must go through ``Decimal(str(value))``: building a Decimal
            from a float reintroduces binary rounding into a monetary conversion.
        reverse_rate: The rate converting in the opposite direction, when the API includes it.
        status: Current status of the rate.
        revision: Revision number.
        audit: Audit information (created, updated, deleted events).
    """

    pair: BaseModel | None
    external_id: str | None
    record_date: str | None
    value: float | None  # noqa: WPS110  # the API's own field name for the rate amount
    reverse_rate: BaseModel | None
    status: str | None
    revision: int | None
    audit: BaseModel | None


class RatesServiceConfig:
    """Rates service configuration."""

    _endpoint = "/public/v1/exchange/pairs/{pair_id}/rates"
    _model_class = Rate
    _collection_key = "data"


class RatesService(
    CreateMixin[Rate],
    GetMixin[Rate],
    UpdateMixin[Rate],
    DeleteMixin,
    CollectionMixin[Rate],
    Service[Rate],
    RatesServiceConfig,
):
    """Rates service."""


class AsyncRatesService(
    AsyncCreateMixin[Rate],
    AsyncGetMixin[Rate],
    AsyncUpdateMixin[Rate],
    AsyncDeleteMixin,
    AsyncCollectionMixin[Rate],
    AsyncService[Rate],
    RatesServiceConfig,
):
    """Async rates service."""
