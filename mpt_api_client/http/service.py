from urllib.parse import urljoin

from mpt_api_client.http.base_service import ServiceBase
from mpt_api_client.http.client import HTTPClient
from mpt_api_client.http.types import QueryParam, Response
from mpt_api_client.models import Model as BaseModel
from mpt_api_client.models import ResourceData
from mpt_api_client.models.collection import ResourceList


class Service[Model: BaseModel](ServiceBase[HTTPClient, Model]):  # noqa: WPS214
    """Immutable service for RESTful resource collections.

    Examples:
        active_orders_cc = order_collection.filter(RQLQuery(status="active"))
        active_orders = active_orders_cc.order_by("created").iterate()
        product_active_orders = active_orders_cc.filter(RQLQuery(product__id="PRD-1")).iterate()

        new_order = order_collection.create(order_data)

    """

    def _resource_do_request(  # noqa: WPS211
        self,
        resource_id: str,
        method: str = "GET",
        action: str | None = None,
        json: ResourceData | ResourceList | None = None,
        query_params: QueryParam | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """Perform an action on a specific resource using `HTTP_METHOD /endpoint/{resource_id}`.

        Args:
            resource_id: The resource ID to operate on.
            method: The HTTP method to use.
            action: The action name to use.
            json: The updated resource data.
            query_params: Additional query parameters.
            headers: Additional headers.

        Returns:
            HTTP response object.

        Raises:
            HTTPError: If the action fails.
        """
        resource_url = urljoin(f"{self.path}/", resource_id)
        url = urljoin(f"{resource_url}/", action) if action else resource_url
        return self.http_client.request(
            method, url, json=json, query_params=query_params, headers=headers
        )

    def _resource_action(
        self,
        resource_id: str,
        method: str = "GET",
        action: str | None = None,
        json: ResourceData | ResourceList | None = None,
        query_params: QueryParam | None = None,
    ) -> Model:
        """Perform an action on a specific resource using `HTTP_METHOD /endpoint/{resource_id}`.

        Args:
            resource_id: The resource ID to operate on.
            method: The HTTP method to use.
            action: The action name to use.
            json: The updated resource data.
            query_params: Additional query parameters.
        """
        response = self._resource_do_request(
            resource_id,
            method,
            action,
            json=json,
            query_params=query_params,
            headers={"Accept": "application/json"},
        )
        return self._model_class.from_response(response)
