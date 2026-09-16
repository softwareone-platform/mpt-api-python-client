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
from mpt_api_client.resources.exchange.rates import AsyncRatesService, RatesService


class Pair(Model):
    """Currency pair resource.

    Attributes:
        name: Pair name auto-generated from the ISO codes of both currencies, for example
            ``"VND:USD"``.
        external_id: Identifier within the external system.
        source_currency: Reference to the source currency, carrying its ISO ``code``.
        destination_currency: Reference to the destination currency, carrying its ISO ``code``.
        notes: Optional text provided when the pair was created.
        latest_rate: The most recent rate of exchange from source to destination, whose amount
            is under ``value``.
        agreements: Number of agreements currently using this pair.
        rates: Number of rates recorded for this pair.
        primary: Whether this is the primary direction of the pair.
        reverse: The pair converting in the opposite direction, including its own
            ``latest_rate``, so both directions arrive in one response.
        status: Current status of the pair.
        revision: Revision number.
        audit: Audit information (created, updated, deleted events).

    Note:
        Filters use the API's own property paths, which are ``sourceCurrency.code`` and
        ``destinationCurrency.code``; the API rejects any other spelling with a 400.
    """

    name: str | None
    external_id: str | None
    source_currency: BaseModel | None
    destination_currency: BaseModel | None
    notes: str | None
    latest_rate: BaseModel | None
    agreements: int | None
    rates: int | None
    primary: bool | None
    reverse: BaseModel | None
    status: str | None
    revision: int | None
    audit: BaseModel | None


class PairsServiceConfig:
    """Pairs service configuration."""

    _endpoint = "/public/v1/exchange/pairs"
    _model_class = Pair
    _collection_key = "data"


class PairsService(
    CreateMixin[Pair],
    GetMixin[Pair],
    UpdateMixin[Pair],
    DeleteMixin,
    CollectionMixin[Pair],
    Service[Pair],
    PairsServiceConfig,
):
    """Pairs service."""

    def rates(self, pair_id: str) -> RatesService:
        """Return the rates service for the given currency pair.

        Args:
            pair_id: Currency pair ID.

        Returns:
            Rates service scoped to that pair.
        """
        return RatesService(
            http_client=self.http_client,
            endpoint_params={"pair_id": pair_id},
        )


class AsyncPairsService(
    AsyncCreateMixin[Pair],
    AsyncGetMixin[Pair],
    AsyncUpdateMixin[Pair],
    AsyncDeleteMixin,
    AsyncCollectionMixin[Pair],
    AsyncService[Pair],
    PairsServiceConfig,
):
    """Async pairs service."""

    def rates(self, pair_id: str) -> AsyncRatesService:
        """Return the rates service for the given currency pair.

        Args:
            pair_id: Currency pair ID.

        Returns:
            Async rates service scoped to that pair.
        """
        return AsyncRatesService(
            http_client=self.http_client,
            endpoint_params={"pair_id": pair_id},
        )
