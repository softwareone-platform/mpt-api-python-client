from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model


class OrdersAsset(Model):
    """Orders Asset resource."""


class OrdersAssetServiceConfig:
    """Orders Asset service config."""

    _endpoint = "/public/v1/commerce/orders/{order_id}/assets"
    _model_class = OrdersAsset
    _collection_key = "data"


class OrdersAssetService(  # noqa: WPS215
    ManagedResourceMixin[OrdersAsset],
    CollectionMixin[OrdersAsset],
    Service[OrdersAsset],
    OrdersAssetServiceConfig,
):
    """Orders Asset service."""

    def render(self, resource_id: str) -> str:
        """Render order asset template.

        Args:
            resource_id: Order asset resource ID

        Returns:
            Order asset template text in markdown format.
        """
        response = self._resource_do_request(
            resource_id,
            "GET",
            "render",
        )
        return response.text


class AsyncOrdersAssetService(  # noqa: WPS215
    AsyncManagedResourceMixin[OrdersAsset],
    AsyncCollectionMixin[OrdersAsset],
    AsyncService[OrdersAsset],
    OrdersAssetServiceConfig,
):
    """Async Orders Asset service."""

    async def render(self, resource_id: str) -> str:
        """Render order asset template.

        Args:
            resource_id: Order asset resource ID

        Returns:
            Order asset template text in markdown format.
        """
        response = await self._resource_do_request(
            resource_id,
            "GET",
            "render",
        )
        return response.text
