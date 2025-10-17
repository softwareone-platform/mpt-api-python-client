from mpt_api_client.http import (
    AsyncService,
    Service,
)
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncGetMixin,
    CollectionMixin,
    CreateMixin,
    DeleteMixin,
    GetMixin,
)
from mpt_api_client.models import Model, ResourceData


class Subscription(Model):
    """Subscription resource."""


class SubscriptionsServiceConfig:
    """Subscription service config."""

    _endpoint = "/public/v1/commerce/subscriptions"
    _model_class = Subscription
    _collection_key = "data"


class SubscriptionsService(  # noqa: WPS215
    CreateMixin[Subscription],
    DeleteMixin,
    GetMixin[Subscription],
    CollectionMixin[Subscription],
    Service[Subscription],
    SubscriptionsServiceConfig,
):
    """Subscription service."""

    def render(self, resource_id: str) -> str:
        """Render subscription template.

        Args:
            resource_id: Subscription resource ID

        Returns:
            Order template text in markdown format.
        """
        response = self._resource_do_request(resource_id, "GET", "render")
        return response.text

    def terminate(self, resource_id: str, resource_data: ResourceData) -> Subscription:
        """Terminate subscription.

        Args:
            resource_id: Order resource ID
            resource_data: Order resource data

        Returns:
            Subscription template text in markdown format.
        """
        return self._resource_action(resource_id, "POST", "terminate", json=resource_data)


class AsyncSubscriptionsService(  # noqa: WPS215
    AsyncCreateMixin[Subscription],
    AsyncDeleteMixin,
    AsyncGetMixin[Subscription],
    AsyncCollectionMixin[Subscription],
    AsyncService[Subscription],
    SubscriptionsServiceConfig,
):
    """Async Subscription service."""

    async def render(self, resource_id: str) -> str:
        """Render subscription template.

        Args:
            resource_id: Subscription resource ID

        Returns:
            Order template text in markdown format.
        """
        response = await self._resource_do_request(resource_id, "GET", "render")
        return response.text

    async def terminate(self, resource_id: str, resource_data: ResourceData) -> Subscription:
        """Terminate subscription.

        Args:
            resource_id: Order resource ID
            resource_data: Order resource data

        Returns:
            Subscription template text in markdown format.
        """
        return await self._resource_action(resource_id, "POST", "terminate", json=resource_data)
