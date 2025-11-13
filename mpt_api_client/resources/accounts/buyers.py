from typing import override

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateWithIconMixin,
    AsyncDeleteMixin,
    AsyncGetMixin,
    AsyncUpdateWithIconMixin,
    CollectionMixin,
    CreateWithIconMixin,
    DeleteMixin,
    GetMixin,
    UpdateWithIconMixin,
)
from mpt_api_client.http.types import FileTypes
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
    CreateWithIconMixin[Buyer],
    UpdateWithIconMixin[Buyer],
    GetMixin[Buyer],
    DeleteMixin,
    ActivatableMixin[Buyer],
    EnablableMixin[Buyer],
    ValidateMixin[Buyer],
    CollectionMixin[Buyer],
    Service[Buyer],
    BuyersServiceConfig,
):
    """Buyers Service."""

    @override
    def create(
        self,
        resource_data: ResourceData,
        logo: FileTypes,
        data_key: str = "buyer",
        icon_key: str = "logo",
    ) -> Buyer:
        """Create a buyer.

        Args:
            resource_data (ResourceData): Buyer data.
            logo: Logo image in jpg, png, GIF, etc.
            data_key: The key for the buyer data.
            icon_key: The key for the logo image.

        Returns:
            Buyer: Created buyer
        """
        return super().create(
            resource_data=resource_data,
            icon=logo,
            data_key=data_key,
            icon_key=icon_key,
        )

    @override
    def update(
        self,
        resource_id: str,
        resource_data: ResourceData,
        logo: FileTypes,
        data_key: str = "buyer",
        icon_key: str = "logo",
    ) -> Buyer:
        """Update a buyer.

        Args:
            resource_id: Resource ID
            resource_data (ResourceData): Buyer data.
            logo: Logo image in jpg, png, GIF, etc.
            data_key: The key for the buyer data.
            icon_key: The key for the logo image.

        Returns:
            Buyer: Updated buyer
        """
        return super().update(
            resource_id=resource_id,
            resource_data=resource_data,
            icon=logo,
            data_key=data_key,
            icon_key=icon_key,
        )

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
    AsyncCreateWithIconMixin[Buyer],
    AsyncUpdateWithIconMixin[Buyer],
    AsyncGetMixin[Buyer],
    AsyncDeleteMixin,
    AsyncActivatableMixin[Buyer],
    AsyncEnablableMixin[Buyer],
    AsyncValidateMixin[Buyer],
    AsyncCollectionMixin[Buyer],
    AsyncService[Buyer],
    BuyersServiceConfig,
):
    """Async Buyers Service."""

    @override
    async def create(
        self,
        resource_data: ResourceData,
        logo: FileTypes,
        data_key: str = "buyer",
        icon_key: str = "logo",
    ) -> Buyer:
        """Create a buyer.

        Args:
            resource_data (ResourceData): Buyer data.
            logo: Logo image in jpg, png, GIF, etc.
            data_key: The key for the buyer data.
            icon_key: The key for the logo image.

        Returns:
            Buyer: Created buyer
        """
        return await super().create(
            resource_data=resource_data,
            icon=logo,
            data_key=data_key,
            icon_key=icon_key,
        )

    @override
    async def update(
        self,
        resource_id: str,
        resource_data: ResourceData,
        logo: FileTypes,
        data_key: str = "buyer",
        icon_key: str = "logo",
    ) -> Buyer:
        """Update a buyer.

        Args:
            resource_id: Resource ID
            resource_data (ResourceData): Buyer data.
            logo: Logo image in jpg, png, GIF, etc.
            data_key: The key for the buyer data.
            icon_key: The key for the logo image.

        Returns:
            Buyer: Updated buyer
        """
        return await super().update(
            resource_id=resource_id,
            resource_data=resource_data,
            icon=logo,
            data_key=data_key,
            icon_key=icon_key,
        )

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
