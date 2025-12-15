from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateFileMixin,
    AsyncDeleteMixin,
    AsyncDisableMixin,
    AsyncEnableMixin,
    AsyncGetMixin,
    AsyncUpdateFileMixin,
    CollectionMixin,
    CreateFileMixin,
    DeleteMixin,
    DisableMixin,
    EnableMixin,
    GetMixin,
    UpdateFileMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import ResourceData
from mpt_api_client.resources.accounts.mixins import (
    ActivatableMixin,
    AsyncActivatableMixin,
    AsyncValidateMixin,
    ValidateMixin,
)


class Buyer(Model):
    """Buyer Model."""


class BuyersServiceConfig:
    """Buyers Service Configuration."""

    _endpoint = "/public/v1/accounts/buyers"
    _model_class = Buyer
    _collection_key = "data"
    _upload_file_key = "logo"
    _upload_data_key = "buyer"


class BuyersService(
    CreateFileMixin[Buyer],
    UpdateFileMixin[Buyer],
    ActivatableMixin[Buyer],
    EnableMixin[Buyer],
    DisableMixin[Buyer],
    ValidateMixin[Buyer],
    GetMixin[Buyer],
    DeleteMixin,
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
    AsyncCreateFileMixin[Buyer],
    AsyncUpdateFileMixin[Buyer],
    AsyncActivatableMixin[Buyer],
    AsyncEnableMixin[Buyer],
    AsyncDisableMixin[Buyer],
    AsyncValidateMixin[Buyer],
    AsyncGetMixin[Buyer],
    AsyncDeleteMixin,
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
