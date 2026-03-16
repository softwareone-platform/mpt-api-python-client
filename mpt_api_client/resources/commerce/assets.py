from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateMixin,
    AsyncGetMixin,
    AsyncUpdateMixin,
    CollectionMixin,
    CreateMixin,
    GetMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.commerce.mixins import (
    AsyncRenderMixin,
    AsyncTerminateMixin,
    RenderMixin,
    TerminateMixin,
)


class Asset(Model):
    """Asset resource.

    Attributes:
        name: Asset name.
        status: Asset status.
        external_ids: External identifiers.
        price: Price information.
        template: Reference to the template.
        parameters: Asset parameters.
        terms: Reference to terms and conditions.
        agreement: Reference to the agreement.
        product: Reference to the product.
        price_list: Reference to the price list.
        listing: Reference to the listing.
        licensee: Reference to the licensee.
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
    agreement: BaseModel | None
    product: BaseModel | None
    price_list: BaseModel | None
    listing: BaseModel | None
    licensee: BaseModel | None
    lines: list[BaseModel] | None
    audit: BaseModel | None


class AssetTemplate(Model):
    """Asset template resource."""


class AssetServiceConfig:
    """Assets service config."""

    _endpoint = "/public/v1/commerce/assets"
    _model_class = Asset
    _collection_key = "data"


class AssetService(
    CreateMixin[Asset],
    UpdateMixin[Asset],
    GetMixin[Asset],
    TerminateMixin[Asset],
    RenderMixin[Asset],
    CollectionMixin[Asset],
    Service[Asset],
    AssetServiceConfig,
):
    """Assets service."""


class AsyncAssetService(
    AsyncCreateMixin[Asset],
    AsyncUpdateMixin[Asset],
    AsyncGetMixin[Asset],
    AsyncTerminateMixin[Asset],
    AsyncRenderMixin[Asset],
    AsyncCollectionMixin[Asset],
    AsyncService[Asset],
    AssetServiceConfig,
):
    """Asynchronous Assets service."""
