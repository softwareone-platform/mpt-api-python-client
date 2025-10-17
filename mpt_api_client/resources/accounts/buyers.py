from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import ResourceData
from mpt_api_client.resources.accounts.mixins import (
    ActivatableMixin,
    AsyncActivatableMixin,
    AsyncEnablableMixin,
    AsyncValidateMixin,
    EnablableMixin,
    ValidateMixin,
)


class Buyer(Model):
    """Buyer Model."""


class BuyersServiceConfig:
    """Buyers Service Configuration."""

    _endpoint = "/public/v1/accounts/buyers"
    _model_class = Buyer
    _collection_key = "data"


class BuyersService(
    ActivatableMixin[Buyer],
    EnablableMixin[Buyer],
    ValidateMixin[Buyer],
    ManagedResourceMixin[Buyer],
    CollectionMixin[Buyer],
    Service[Buyer],
    BuyersServiceConfig,
):
    """Buyers Service."""

    def synchronize(self, resource_id: str, resource_data: ResourceData | None = None) -> Buyer:
        """Synchronize a buyer.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(resource_id, "POST", "synchronize", json=resource_data)

    def transfer(self, resource_id: str, resource_data: ResourceData | None = None) -> Buyer:
        """Transfer a buyer.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(resource_id, "POST", "transfer", json=resource_data)


class AsyncBuyersService(
    AsyncActivatableMixin[Buyer],
    AsyncEnablableMixin[Buyer],
    AsyncValidateMixin[Buyer],
    AsyncManagedResourceMixin[Buyer],
    AsyncCollectionMixin[Buyer],
    AsyncService[Buyer],
    BuyersServiceConfig,
):
    """Async Buyers Service."""

    async def synchronize(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Buyer:
        """Synchronize a buyer.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(resource_id, "POST", "synchronize", json=resource_data)

    async def transfer(self, resource_id: str, resource_data: ResourceData | None = None) -> Buyer:
        """Transfer a buyer.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(resource_id, "POST", "transfer", json=resource_data)
