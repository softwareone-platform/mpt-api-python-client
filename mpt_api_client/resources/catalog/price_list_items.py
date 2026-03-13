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
from mpt_api_client.models.model import BaseModel


class PriceListItem(Model):
    """Price List Item resource.

    Attributes:
        status: Price list item status.
        description: Price list item description.
        reason_for_change: Reason for the price change.
        unit_lp: Unit list price.
        unit_pp: Unit purchase price.
        markup: Markup percentage.
        margin: Margin percentage.
        unit_sp: Unit sell price.
        ppx1: Purchase price for 1-year term.
        ppxm: Purchase price for monthly term.
        ppxy: Purchase price for yearly term.
        spx1: Sell price for 1-year term.
        spxm: Sell price for monthly term.
        spxy: Sell price for yearly term.
        lpx1: List price for 1-year term.
        lpxm: List price for monthly term.
        lpxy: List price for yearly term.
        price_list: Reference to the parent price list.
        item: Reference to the associated item.
        audit: Audit information (created, updated events).
    """

    status: str | None
    description: str | None
    reason_for_change: str | None
    unit_lp: float | None
    unit_pp: float | None
    markup: float | None
    margin: float | None
    unit_sp: float | None
    ppx1: float | None
    ppxm: float | None
    ppxy: float | None
    spx1: float | None
    spxm: float | None
    spxy: float | None
    lpx1: float | None
    lpxm: float | None
    lpxy: float | None
    price_list: BaseModel | None
    item: BaseModel | None
    audit: BaseModel | None


class PriceListItemsServiceConfig:
    """Price List Items service configuration."""

    _endpoint = "/public/v1/catalog/price-lists/{price_list_id}/items"
    _model_class = PriceListItem
    _collection_key = "data"


class PriceListItemsService(
    GetMixin[PriceListItem],
    UpdateMixin[PriceListItem],
    CollectionMixin[PriceListItem],
    Service[PriceListItem],
    PriceListItemsServiceConfig,
):
    """Price List Items service."""


class AsyncPriceListItemsService(
    AsyncGetMixin[PriceListItem],
    AsyncUpdateMixin[PriceListItem],
    AsyncCollectionMixin[PriceListItem],
    AsyncService[PriceListItem],
    PriceListItemsServiceConfig,
):
    """Price List Items service."""
