from mpt_api_client.http import (
    AsyncService,
    Service,
)
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model, ResourceData
from mpt_api_client.resources.commerce.orders_subscription import (
    AsyncOrderSubscriptionsService,
    OrderSubscriptionsService,
)


class Order(Model):
    """Order resource."""


class OrdersServiceConfig:
    """Orders service config."""

    _endpoint = "/public/v1/commerce/orders"
    _model_class = Order
    _collection_key = "data"


class OrdersService(  # noqa: WPS215 WPS214
    ManagedResourceMixin[Order],
    CollectionMixin[Order],
    Service[Order],
    OrdersServiceConfig,
):
    """Orders service."""

    def validate(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Switch order to validate state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated
        """
        return self._resource_action(resource_id, "POST", "validate", json=resource_data)

    def process(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Switch order to process state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated
        """
        return self._resource_action(resource_id, "POST", "process", json=resource_data)

    def query(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Switch order to query state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated
        """
        return self._resource_action(resource_id, "POST", "query", json=resource_data)

    def complete(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Switch order to complete state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated
        """
        return self._resource_action(resource_id, "POST", "complete", json=resource_data)

    def fail(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Switch order to fail state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated
        """
        return self._resource_action(resource_id, "POST", "fail", json=resource_data)

    def notify(self, resource_id: str, user: ResourceData) -> None:
        """Notify user about order status.

        Args:
            resource_id: Order resource ID
            user: User data
        """
        self._resource_do_request(resource_id, "POST", "notify", json=user)

    def template(self, resource_id: str) -> str:
        """Render order template.

        Args:
            resource_id: Order resource ID

        Returns:
            Order template text in markdown format.
        """
        response = self._resource_do_request(resource_id, "GET", "template")
        return response.text

    def subscriptions(self, order_id: str) -> OrderSubscriptionsService:
        """Get the subscription service for the given Order id.

        Args:
            order_id: Order ID.

        Returns:
            Order Subscription service.
        """
        return OrderSubscriptionsService(
            http_client=self.http_client,
            endpoint_params={"order_id": order_id},
        )


class AsyncOrdersService(  # noqa: WPS215 WPS214
    AsyncManagedResourceMixin[Order],
    AsyncCollectionMixin[Order],
    AsyncService[Order],
    OrdersServiceConfig,
):
    """Async Orders service."""

    async def validate(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Switch order to validate state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated

        Returns:
            Updated order resource
        """
        return await self._resource_action(resource_id, "POST", "validate", json=resource_data)

    async def process(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Switch order to process state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated

        Returns:
            Updated order resource
        """
        return await self._resource_action(resource_id, "POST", "process", json=resource_data)

    async def query(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Switch order to query state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated

        Returns:
            Updated order resource
        """
        return await self._resource_action(resource_id, "POST", "query", json=resource_data)

    async def complete(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Switch order to complete state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated

        Returns:
            Updated order resource
        """
        return await self._resource_action(resource_id, "POST", "complete", json=resource_data)

    async def fail(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Switch order to fail state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated

        Returns:
            Updated order resource
        """
        return await self._resource_action(resource_id, "POST", "fail", json=resource_data)

    async def notify(self, resource_id: str, resource_data: ResourceData) -> None:
        """Notify user about order status.

        Args:
            resource_id: Order resource ID
            resource_data: User data to notify
        """
        await self._resource_do_request(resource_id, "POST", "notify", json=resource_data)

    async def template(self, resource_id: str) -> str:
        """Render order template.

        Args:
            resource_id: Order resource ID

        Returns:
            Order template text in markdown format.
        """
        response = await self._resource_do_request(resource_id, "GET", "template")
        return response.text

    def subscriptions(self, order_id: str) -> AsyncOrderSubscriptionsService:
        """Get the subscription service for the given Order id.

        Args:
            order_id: Order ID.

        Returns:
            Order Subscription service.
        """
        return AsyncOrderSubscriptionsService(
            http_client=self.http_client,
            endpoint_params={"order_id": order_id},
        )
