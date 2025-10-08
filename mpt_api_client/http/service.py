from collections.abc import Iterator
from urllib.parse import urljoin

import httpx

from mpt_api_client.http.base_service import ServiceBase
from mpt_api_client.http.client import HTTPClient
from mpt_api_client.http.types import QueryParam
from mpt_api_client.models import Collection, ResourceData
from mpt_api_client.models import Model as BaseModel
from mpt_api_client.models.collection import ResourceList


class Service[Model: BaseModel](ServiceBase[HTTPClient, Model]):  # noqa: WPS214
    """Immutable service for RESTful resource collections.

    Examples:
        active_orders_cc = order_collection.filter(RQLQuery(status="active"))
        active_orders = active_orders_cc.order_by("created").iterate()
        product_active_orders = active_orders_cc.filter(RQLQuery(product__id="PRD-1")).iterate()

        new_order = order_collection.create(order_data)

    """

    def fetch_page(self, limit: int = 100, offset: int = 0) -> Collection[Model]:
        """Fetch one page of resources.

        Returns:
            Collection of resources.
        """
        response = self._fetch_page_as_response(limit=limit, offset=offset)
        return self._create_collection(response)

    def fetch_one(self) -> Model:
        """Fetch one resource, expect exactly one result.

        Returns:
            One resource.

        Raises:
            ValueError: If the total matching records are not exactly one.
        """
        response = self._fetch_page_as_response(limit=1, offset=0)
        resource_list = self._create_collection(response)
        total_records = len(resource_list)
        if resource_list.meta:
            total_records = resource_list.meta.pagination.total
        if total_records == 0:
            raise ValueError("Expected one result, but got zero results")
        if total_records > 1:
            raise ValueError(f"Expected one result, but got {total_records} results")

        return resource_list[0]

    def iterate(self, batch_size: int = 100) -> Iterator[Model]:
        """Iterate over all resources, yielding GenericResource objects.

        Args:
            batch_size: Number of resources to fetch per request

        Returns:
            Iterator of resources.
        """
        offset = 0
        limit = batch_size  # Default page size

        while True:
            response = self._fetch_page_as_response(limit=limit, offset=offset)
            items_collection = self._create_collection(response)
            yield from items_collection

            if not items_collection.meta:
                break
            if not items_collection.meta.pagination.has_next():
                break
            offset = items_collection.meta.pagination.next_offset()

    def get(self, resource_id: str, select: list[str] | str | None = None) -> Model:
        """Fetch a specific resource using `GET /endpoint/{resource_id}`.

        Args:
            resource_id: Resource ID.
            select: List of fields to select.

        Returns:
            Resource object.
        """
        if isinstance(select, list):
            select = ",".join(select) if select else None

        return self._resource_action(resource_id=resource_id, query_params={"select": select})

    def _fetch_page_as_response(self, limit: int = 100, offset: int = 0) -> httpx.Response:
        """Fetch one page of resources.

        Returns:
            httpx.Response object.

        Raises:
            HTTPStatusError: if the response status code is not 200.
        """
        pagination_params: dict[str, int] = {"limit": limit, "offset": offset}
        return self.http_client.get(self.build_url(pagination_params))

    def _resource_do_request(  # noqa: WPS211
        self,
        resource_id: str,
        method: str = "GET",
        action: str | None = None,
        json: ResourceData | ResourceList | None = None,
        query_params: QueryParam | None = None,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
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
        resource_url = urljoin(f"{self.endpoint}/", resource_id)
        url = urljoin(f"{resource_url}/", action) if action else resource_url
        return self.http_client.request(
            method, url, json=json, params=query_params, headers=headers
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
