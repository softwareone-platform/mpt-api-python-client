from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.commerce.mixins import AsyncRenderMixin, RenderMixin


class OrdersAsset(Model):
    """Orders Asset resource.

    Attributes:
        name: Asset name.
        status: Asset status.
        external_ids: External identifiers.
        price: Price information.
        template: Reference to the template.
        parameters: Asset parameters.
        terms: Reference to terms and conditions.
        lines: List of asset lines.
        audit: Audit information.
    """

    name: str | None
    status: str | None
    external_ids: BaseModel | None
    price: BaseModel | None
    template: BaseModel | None
    parameters: BaseModel | None  # noqa: WPS110
    terms: BaseModel | None
    lines: list[BaseModel] | None
    audit: BaseModel | None


class OrdersAssetServiceConfig:
    """Orders Asset service config."""

    _endpoint = "/public/v1/commerce/orders/{order_id}/assets"
    _model_class = OrdersAsset
    _collection_key = "data"


class OrdersAssetService(  # noqa: WPS215
    RenderMixin[OrdersAsset],
    ManagedResourceMixin[OrdersAsset],
    CollectionMixin[OrdersAsset],
    Service[OrdersAsset],
    OrdersAssetServiceConfig,
):
    """Orders Asset service."""


class AsyncOrdersAssetService(  # noqa: WPS215
    AsyncRenderMixin[OrdersAsset],
    AsyncManagedResourceMixin[OrdersAsset],
    AsyncCollectionMixin[OrdersAsset],
    AsyncService[OrdersAsset],
    OrdersAssetServiceConfig,
):
    """Async Orders Asset service."""
