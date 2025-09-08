from mpt_api_client.http import (
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncService,
    AsyncUpdateMixin,
    CreateMixin,
    DeleteMixin,
    Service,
    UpdateMixin,
)
from mpt_api_client.models import Model, ResourceData
from mpt_api_client.resources.commerce.mixins import (
    AsyncCompleteMixin,
    AsyncFailMixin,
    AsyncProcessMixin,
    AsyncQueryMixin,
    AsyncTemplateMixin,
    AsyncValidateMixin,
    CompleteMixin,
    FailMixin,
    ProcessMixin,
    QueryMixin,
    TemplateMixin,
    ValidateMixin,
)
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


class OrdersService(
    CreateMixin[Order],
    DeleteMixin,
    UpdateMixin[Order],
    ValidateMixin[Order],
    ProcessMixin[Order],
    QueryMixin[Order],
    TemplateMixin,
    CompleteMixin[Order],
    FailMixin[Order],
    Service[Order],
    OrdersServiceConfig,
):
    """Orders service."""

    def notify(self, resource_id: str, user: ResourceData) -> None:
        """Notify user about order status.

        Args:
            resource_id: Order resource ID
            user: User data
        """
        self._resource_do_request(resource_id, "POST", "notify", json=user)

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


class AsyncOrdersService(
    AsyncCreateMixin[Order],
    AsyncDeleteMixin,
    AsyncUpdateMixin[Order],
    AsyncValidateMixin[Order],
    AsyncProcessMixin[Order],
    AsyncQueryMixin[Order],
    AsyncCompleteMixin[Order],
    AsyncFailMixin[Order],
    AsyncTemplateMixin,
    AsyncService[Order],
    OrdersServiceConfig,
):
    """Async Orders service."""

    async def notify(self, resource_id: str, resource_data: ResourceData) -> None:
        """Notify user about order status.

        Args:
            resource_id: Order resource ID
            resource_data: User data to notify
        """
        await self._resource_do_request(resource_id, "POST", "notify", json=resource_data)

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
