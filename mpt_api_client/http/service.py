from mpt_api_client.http.base_service import ServiceBase
from mpt_api_client.http.client import HTTPClient
from mpt_api_client.http.resource_accessor import ResourceAccessor
from mpt_api_client.http.url_utils import join_url_path
from mpt_api_client.models import Model as BaseModel


class Service[Model: BaseModel](ServiceBase[HTTPClient, Model]):  # noqa: WPS214
    """Immutable service for RESTful resource collections.

    Examples:
        active_orders_cc = order_collection.filter(RQLQuery(status="active"))
        active_orders = active_orders_cc.order_by("created").iterate()
        product_active_orders = active_orders_cc.filter(RQLQuery(product__id="PRD-1")).iterate()

        new_order = order_collection.create(order_data)

    """

    def _resource(self, resource_id: str) -> ResourceAccessor[Model]:
        """Return a :class:`ResourceAccessor` bound to *resource_id*.

        Usage::

            self._resource("RES-123").post("complete", json=data)
            self._resource("RES-123").get()
            self._resource("RES-123").put(json=data)
            self._resource("RES-123").delete()
        """
        resource_url = join_url_path(self.path, resource_id)
        return ResourceAccessor(self.http_client, resource_url, self._model_class)
