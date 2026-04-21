from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncGetMixin,
    CollectionMixin,
    GetMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class SpotlightObject(Model):
    """Spotlight Object resource.

    Attributes:
        id: Unique identifier for the spotlight object.
        total: Total number of spotlight objects.
        top: Top spotlight objects.
        query: Spotlight queries.
    """

    id: str = ""
    total: int | None
    top: BaseModel | None
    query: BaseModel | None


class SpotlightObjectsServiceConfig:
    """Configuration for Spotlight Objects Service.

    Attributes:
        endpoint: API endpoint for spotlight objects.
    """

    _endpoint: str = "/public/v1/spotlight/objects"
    _model_class = SpotlightObject
    _collection_key = "data"


class SpotlightObjectsService(
    GetMixin[SpotlightObject],
    CollectionMixin[SpotlightObject],
    Service[SpotlightObject],
    SpotlightObjectsServiceConfig,
):
    """Service for managing spotlight objects."""

    def refresh(self, object_id: str = "-") -> None:
        """Refresh a spotlight object.

        Args:
            object_id: The ID of the spotlight object to refresh.
        """
        self._resource(object_id).do_request("POST", "refresh")


class AsyncSpotlightObjectsService(
    AsyncGetMixin[SpotlightObject],
    AsyncCollectionMixin[SpotlightObject],
    AsyncService[SpotlightObject],
    SpotlightObjectsServiceConfig,
):
    """Asynchronous service for managing spotlight objects."""

    async def refresh(self, object_id: str = "-") -> None:
        """Refresh a spotlight object.

        Args:
            object_id: The ID of the spotlight object to refresh.
        """
        await self._resource(object_id).do_request("POST", "refresh")
