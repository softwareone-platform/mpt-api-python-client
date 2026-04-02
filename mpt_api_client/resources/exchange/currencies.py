from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateFileMixin,
    AsyncDeleteMixin,
    AsyncGetMixin,
    AsyncUpdateFileMixin,
    CollectionMixin,
    CreateFileMixin,
    DeleteMixin,
    GetMixin,
    UpdateFileMixin,
)
from mpt_api_client.models import FileModel, Model
from mpt_api_client.models.model import BaseModel


class Currency(Model):
    """Currency resource.

    Attributes:
        name: Currency name.
        code: ISO code of the currency.
        precision: Number of decimal places.
        statistics: Currency statistics (seller count, pair count).
        status: Current status of the currency.
        icon: URL or identifier for the currency icon.
        revision: Revision number.
        audit: Audit information (created, updated events).
    """

    name: str | None
    code: str | None
    precision: int | None
    statistics: BaseModel | None
    status: str | None
    icon: str | None
    revision: int | None
    audit: BaseModel | None


class CurrenciesServiceConfig:
    """Currencies service configuration."""

    _endpoint = "/public/v1/exchange/currencies"
    _model_class = Currency
    _collection_key = "data"
    _upload_file_key = "icon"
    _upload_data_key = "currency"


class CurrenciesService(
    CreateFileMixin[Currency],
    GetMixin[Currency],
    UpdateFileMixin[Currency],
    DeleteMixin,
    CollectionMixin[Currency],
    Service[Currency],
    CurrenciesServiceConfig,
):
    """Currencies service."""

    def download_icon(self, resource_id: str) -> FileModel:
        """Download the icon for the given currency.

        Args:
            resource_id: Currency ID.

        Returns:
            File model containing the downloaded icon.
        """
        response = self._resource(resource_id).do_request("GET", "icon")
        return FileModel(response)


class AsyncCurrenciesService(
    AsyncCreateFileMixin[Currency],
    AsyncGetMixin[Currency],
    AsyncUpdateFileMixin[Currency],
    AsyncDeleteMixin,
    AsyncCollectionMixin[Currency],
    AsyncService[Currency],
    CurrenciesServiceConfig,
):
    """Async currencies service."""

    async def download_icon(self, resource_id: str) -> FileModel:
        """Download the icon for the given currency.

        Args:
            resource_id: Currency ID.

        Returns:
            File model containing the downloaded icon.
        """
        response = await self._resource(resource_id).do_request("GET", "icon")
        return FileModel(response)
