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
from mpt_api_client.resources.commerce.mixins import (
    AsyncRenderMixin,
    AsyncTerminateMixin,
    RenderMixin,
    TerminateMixin,
)


class Asset(Model):
    """Asset resource."""


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
