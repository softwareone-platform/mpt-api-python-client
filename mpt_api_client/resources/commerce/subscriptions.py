from mpt_api_client.http import (
    AsyncService,
    Service,
)
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
from mpt_api_client.resources.commerce.mixins import AsyncTerminateMixin, TerminateMixin


class Subscription(Model):
    """Subscription resource."""


class SubscriptionsServiceConfig:
    """Subscription service config."""

    _endpoint = "/public/v1/commerce/subscriptions"
    _model_class = Subscription
    _collection_key = "data"


class SubscriptionsService(  # noqa: WPS215
    CreateMixin[Subscription],
    UpdateMixin[Subscription],
    GetMixin[Subscription],
    CollectionMixin[Subscription],
    TerminateMixin[Subscription],
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


class AsyncSubscriptionsService(  # noqa: WPS215
    AsyncCreateMixin[Subscription],
    AsyncUpdateMixin[Subscription],
    AsyncGetMixin[Subscription],
    AsyncCollectionMixin[Subscription],
    AsyncTerminateMixin[Subscription],
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
