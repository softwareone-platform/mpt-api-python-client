from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncGetMixin,
    AsyncUpdateMixin,
    CreateMixin,
    DeleteMixin,
    GetMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import ResourceData
from mpt_api_client.resources.accounts.mixins import ActivatableMixin, AsyncActivatableMixin


class Seller(Model):
    """Seller Model."""


class SellersServiceConfig:
    """Sellers Service Configuration."""

    _endpoint = "/public/v1/accounts/sellers"
    _model_class = Seller
    _collection_key = "data"


class SellersService(
    CreateMixin[Seller],
    DeleteMixin,
    GetMixin[Seller],
    UpdateMixin[Seller],
    ActivatableMixin[Seller],
    Service[Seller],
    SellersServiceConfig,
):
    """Sellers Service."""

    def disable(self, resource_id: str, resource_data: ResourceData | None = None) -> Seller:
        """Disable a seller.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(resource_id, "POST", "disable", json=resource_data)


class AsyncSellersService(
    AsyncCreateMixin[Seller],
    AsyncDeleteMixin,
    AsyncGetMixin[Seller],
    AsyncUpdateMixin[Seller],
    AsyncActivatableMixin[Seller],
    AsyncService[Seller],
    SellersServiceConfig,
):
    """Async Sellers Service."""

    async def disable(self, resource_id: str, resource_data: ResourceData | None = None) -> Seller:
        """Disable a seller.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(resource_id, "POST", "disable", json=resource_data)
