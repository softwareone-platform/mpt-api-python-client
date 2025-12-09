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
from mpt_api_client.models.model import ResourceData


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
    CollectionMixin[Asset],
    Service[Asset],
    AssetServiceConfig,
):
    """Assets service."""

    def terminate(self, asset_id: str, resource_data: ResourceData | None = None) -> Asset:
        """Terminate the given Asset id.

        Args:
            asset_id: Asset ID.
            resource_data: Resource data will be updated
        """
        response = self._resource_do_request(asset_id, "POST", "terminate", json=resource_data)
        return self._model_class.from_response(response)

    def render(self, asset_id: str) -> str:
        """Renders the template for the given Asset id.

        Args:
            asset_id: Asset ID.

        Returns:
            Render asset template json.
        """
        response = self._resource_do_request(asset_id, action="render")

        return response.text


class AsyncAssetService(
    AsyncCreateMixin[Asset],
    AsyncUpdateMixin[Asset],
    AsyncGetMixin[Asset],
    AsyncCollectionMixin[Asset],
    AsyncService[Asset],
    AssetServiceConfig,
):
    """Asynchronous Assets service."""

    async def terminate(self, asset_id: str, resource_data: ResourceData | None = None) -> Asset:
        """Terminate the given Asset id.

        Args:
            asset_id: Asset ID.
            resource_data: Resource data will be updated
        """
        response = await self._resource_do_request(
            asset_id, "POST", "terminate", json=resource_data
        )

        return self._model_class.from_response(response)

    async def render(self, asset_id: str) -> str:
        """Renders the template for the given Asset id.

        Args:
            asset_id: Asset ID.

        Returns:
            Render asset template string.
        """
        response = await self._resource_do_request(asset_id, action="render")

        return response.text
