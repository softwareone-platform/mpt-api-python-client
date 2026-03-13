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
        p_px1: Purchase price for 1-year term.
        p_px_m: Purchase price for monthly term.
        p_px_y: Purchase price for yearly term.
        s_px1: Sell price for 1-year term.
        s_px_m: Sell price for monthly term.
        s_px_y: Sell price for yearly term.
        l_px1: List price for 1-year term.
        l_px_m: List price for monthly term.
        l_px_y: List price for yearly term.
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
    p_px1: float | None
    p_px_m: float | None
    p_px_y: float | None
    s_px1: float | None
    s_px_m: float | None
    s_px_y: float | None
    l_px1: float | None
    l_px_m: float | None
    l_px_y: float | None
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
