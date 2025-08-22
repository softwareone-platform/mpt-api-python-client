from typing import Any

from mpt_api_client.http.collection import CollectionClientBase
from mpt_api_client.http.resource import ResourceBaseClient
from mpt_api_client.models import Collection, Resource
from mpt_api_client.registry import commerce


class Order(Resource):
    """Order resource."""


class OrderResourceClient(ResourceBaseClient[Order]):
    """Order resource client."""

    _endpoint = "/public/v1/commerce/orders"
    _resource_class = Order

    def validate(self, order: dict[str, Any] | None = None) -> Order:
        """Switch order to validate state.

        Args:
            order: Order data will be updated
        """
        response = self._do_action("POST", "validate", json=order)
        return self._resource_class.from_response(response)

    def process(self, order: dict[str, Any] | None = None) -> Order:
        """Switch order to process state.

        Args:
            order: Order data will be updated
        """
        return self._resource_action("POST", "process", json=order)

    def query(self, order: dict[str, Any] | None = None) -> Order:
        """Switch order to query state.

        Args:
            order: Order data will be updated
        """
        return self._resource_action("POST", "query", json=order)

    def complete(self, order: dict[str, Any] | None = None) -> Order:
        """Switch order to complete state.

        Args:
            order: Order data will be updated
        """
        return self._resource_action("POST", "complete", json=order)

    def fail(self, order: dict[str, Any] | None = None) -> Order:
        """Switch order to fail state.

        Args:
            order: Order data will be updated
        """
        return self._resource_action("POST", "fail", json=order)

    def notify(self, user: dict[str, Any]) -> None:
        """Notify user about order status.

        Args:
            user: User data
        """
        self._do_action("POST", "notify", json=user)

    def template(self) -> str:
        """Render order template.

        Returns:
            Order template text in markdown format.
        """
        response = self._do_action("GET", "template")
        return response.text


@commerce("orders")
class OrderCollectionClientBase(CollectionClientBase[Order, OrderResourceClient]):
    """Orders client."""

    _endpoint = "/public/v1/commerce/orders"
    _resource_class = Order
    _resource_client_class = OrderResourceClient
    _collection_class = Collection[Order]
