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
from mpt_api_client.resources.accounts.mixins import AsyncEnablableMixin, EnablableMixin


class Licensee(Model):
    """Licensee Model."""


class LicenseesServiceConfig:
    """Licensees Service Configuration."""

    _endpoint = "/public/v1/accounts/licensees"
    _model_class = Licensee
    _collection_key = "data"


class LicenseesService(
    CreateWithIconMixin[Licensee],
    UpdateWithIconMixin[Licensee],
    GetMixin[Licensee],
    DeleteMixin,
    EnablableMixin[Licensee],
    CollectionMixin[Licensee],
    Service[Licensee],
    LicenseesServiceConfig,
):
    """Licensees Service."""

    @override
    def create(
        self,
        resource_data: ResourceData,
        logo: FileTypes,
        data_key: str = "licensee",
        icon_key: str = "logo",
    ) -> Licensee:
        """Create a licensee.

        Args:
            resource_data (ResourceData): Licensee data.
            logo: Logo image in jpg, png, GIF, etc.
            data_key: The key for the licensee data.
            icon_key: The key for the logo image.

        Returns:
            Licensee: Created licensee
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
        data_key: str = "licensee",
        icon_key: str = "logo",
    ) -> Licensee:
        """Update a licensee.

        Args:
            resource_id (str): Licensee ID.
            resource_data (ResourceData): Licensee data.
            logo: Logo image in jpg, png, GIF, etc.
            data_key: The key for the licensee data.
            icon_key: The key for the logo image.

        Returns:
            Licensee: Updated licensee
        """
        return super().update(
            resource_id=resource_id,
            resource_data=resource_data,
            icon=logo,
            data_key=data_key,
            icon_key=icon_key,
        )


class AsyncLicenseesService(
    AsyncCreateWithIconMixin[Licensee],
    AsyncUpdateWithIconMixin[Licensee],
    AsyncGetMixin[Licensee],
    AsyncDeleteMixin,
    AsyncEnablableMixin[Licensee],
    AsyncCollectionMixin[Licensee],
    AsyncService[Licensee],
    LicenseesServiceConfig,
):
    """Async Licensees Service."""

    @override
    async def create(
        self,
        resource_data: ResourceData,
        logo: FileTypes,
        data_key: str = "licensee",
        icon_key: str = "logo",
    ) -> Licensee:
        """Create a licensee.

        Args:
            resource_data (ResourceData): Licensee data.
            logo: Logo image in jpg, png, GIF, etc.
            data_key: The key for the licensee data.
            icon_key: The key for the logo image.

        Returns:
            Licensee: Created licensee
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
        data_key: str = "licensee",
        icon_key: str = "logo",
    ) -> Licensee:
        """Update a licensee.

        Args:
            resource_id (str): Licensee ID.
            resource_data (ResourceData): Licensee data.
            logo: Logo image in jpg, png, GIF, etc.
            data_key: The key for the licensee data.
            icon_key: The key for the logo image.

        Returns:
            Licensee: Updated licensee
        """
        return await super().update(
            resource_id=resource_id,
            resource_data=resource_data,
            icon=logo,
            data_key=data_key,
            icon_key=icon_key,
        )
