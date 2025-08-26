import copy
from collections.abc import AsyncIterator, Iterator
from typing import Any, Self

import httpx

from mpt_api_client.http.client import AsyncHTTPClient, HTTPClient
from mpt_api_client.models import Collection, Meta, Model, ResourceData
from mpt_api_client.models.collection import ResourceList
from mpt_api_client.rql.query_builder import RQLQuery


class ServiceSharedBase[HTTP, ModelClass: Model]:
    """Client base."""

    _endpoint: str
    _model_class: type[ModelClass]
    _collection_key = "data"

    def __init__(
        self,
        *,
        http_client: HTTP,
        query_rql: RQLQuery | None = None,
    ) -> None:
        self.http_client = http_client
        self.query_rql: RQLQuery | None = query_rql
        self.query_order_by: list[str] | None = None
        self.query_select: list[str] | None = None

    def clone(self) -> Self:
        """Create a copy of collection client for immutable operations.

        Returns:
            New collection client with same settings.
        """
        new_collection = type(self)(http_client=self.http_client, query_rql=self.query_rql)
        new_collection.query_order_by = (
            copy.copy(self.query_order_by) if self.query_order_by else None
        )
        new_collection.query_select = copy.copy(self.query_select) if self.query_select else None
        return new_collection

    def build_url(self, query_params: dict[str, Any] | None = None) -> str:  # noqa: WPS210
        """Builds the endpoint URL with all the query parameters.

        Returns:
            Partial URL with query parameters.
        """
        query_params = query_params or {}
        query_parts = [
            f"{param_key}={param_value}" for param_key, param_value in query_params.items()
        ]
        if self.query_order_by:
            str_order_by = ",".join(self.query_order_by)
            query_parts.append(f"order={str_order_by}")
        if self.query_select:
            str_query_select = ",".join(self.query_select)
            query_parts.append(f"select={str_query_select}")
        if self.query_rql:
            query_parts.append(str(self.query_rql))
        if query_parts:
            query = "&".join(query_parts)
            return f"{self._endpoint}?{query}"
        return self._endpoint

    def order_by(self, *fields: str) -> Self:
        """Returns new collection with ordering setup.

        Returns:
            New collection with ordering setup.

        Raises:
            ValueError: If ordering has already been set.
        """
        if self.query_order_by is not None:
            raise ValueError("Ordering is already set. Cannot set ordering multiple times.")
        new_collection = self.clone()
        new_collection.query_order_by = list(fields)
        return new_collection

    def filter(self, rql: RQLQuery) -> Self:
        """Creates a new collection with the filter added to the filter collection.

        Returns:
            New copy of the collection with the filter added.
        """
        if self.query_rql:
            rql = self.query_rql & rql
        new_collection = self.clone()
        new_collection.query_rql = rql
        return new_collection

    def select(self, *fields: str) -> Self:
        """Set select fields. Raises ValueError if select fields are already set.

        Returns:
            New copy of the collection with the select fields set.

        Raises:
            ValueError: If select fields are already set.
        """
        if self.query_select is not None:
            raise ValueError(
                "Select fields are already set. Cannot set select fields multiple times."
            )

        new_client = self.clone()
        new_client.query_select = list(fields)
        return new_client

    def _create_collection(self, response: httpx.Response) -> Collection[ModelClass]:
        meta = Meta.from_response(response)
        return Collection(
            items=[
                self._model_class.new(resource, meta)
                for resource in response.json().get(self._collection_key)
            ],
            meta=meta,
        )


class SyncServiceBase[ModelClass: Model](ServiceSharedBase[HTTPClient, ModelClass]):
    """Immutable Base client for RESTful resource collections.

    Examples:
        active_orders_cc = order_collection.filter(RQLQuery(status="active"))
        active_orders = active_orders_cc.order_by("created").iterate()
        product_active_orders = active_orders_cc.filter(RQLQuery(product__id="PRD-1")).iterate()

        new_order = order_collection.create(order_data)

    """

    def fetch_page(self, limit: int = 100, offset: int = 0) -> Collection[ModelClass]:
        """Fetch one page of resources.

        Returns:
            Collection of resources.
        """
        response = self._fetch_page_as_response(limit=limit, offset=offset)
        return self._create_collection(response)

    def fetch_one(self) -> ModelClass:
        """Fetch one page, expect exactly one result.

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

    def iterate(self, batch_size: int = 100) -> Iterator[ModelClass]:
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

    def create(self, resource_data: ResourceData) -> Model:
        """Create a new resource using `POST /endpoint`.

        Returns:
            New resource created.
        """
        response = self.http_client.post(self._endpoint, json=resource_data)
        response.raise_for_status()

        return self._model_class.from_response(response)

    def get(self, resource_id: str) -> ModelClass:
        """Fetch a specific resource using `GET /endpoint/{resource_id}`."""
        return self._resource_action(resource_id=resource_id)

    def update(self, resource_id: str, resource_data: ResourceData) -> ModelClass:
        """Update a resource using `PUT /endpoint/{resource_id}`."""
        return self._resource_action(resource_id, "PUT", json=resource_data)

    def delete(self, resource_id: str) -> None:
        """Delete the resoruce using `DELETE /endpoint/{resource_id}`."""
        response = self._resource_do_request(resource_id, "DELETE")
        response.raise_for_status()

    def _fetch_page_as_response(self, limit: int = 100, offset: int = 0) -> httpx.Response:
        """Fetch one page of resources.

        Returns:
            httpx.Response object.

        Raises:
            HTTPStatusError: if the response status code is not 200.
        """
        pagination_params: dict[str, int] = {"limit": limit, "offset": offset}
        response = self.http_client.get(self.build_url(pagination_params))
        response.raise_for_status()

        return response

    def _resource_do_request(
        self,
        resource_id: str,
        method: str = "GET",
        action: str | None = None,
        json: ResourceData | ResourceList | None = None,
    ) -> httpx.Response:
        """Perform an action on a specific resource using `HTTP_METHOD /endpoint/{resource_id}`.

        Args:
            resource_id: The resource ID to operate on.
            method: The HTTP method to use.
            action: The action name to use.
            json: The updated resource data.

        Returns:
            HTTP response object.

        Raises:
            HTTPError: If the action fails.
        """
        resource_url = f"{self._endpoint}/{resource_id}"
        url = f"{resource_url}/{action}" if action else resource_url
        response = self.http_client.request(method, url, json=json)
        response.raise_for_status()
        return response

    def _resource_action(
        self,
        resource_id: str,
        method: str = "GET",
        action: str | None = None,
        json: ResourceData | ResourceList | None = None,
    ) -> ModelClass:
        """Perform an action on a specific resource using `HTTP_METHOD /endpoint/{resource_id}`."""
        response = self._resource_do_request(resource_id, method, action, json=json)
        return self._model_class.from_response(response)


class AsyncServiceBase[  # noqa: WPS214
    ModelClass: Model,
](  # noqa: WPS214
    ServiceSharedBase[AsyncHTTPClient, ModelClass]
):
    """Immutable Base client for RESTful resource collections.

    Examples:
        active_orders_cc = order_collection.filter(RQLQuery(status="active"))
        active_orders = active_orders_cc.order_by("created").iterate()
        product_active_orders = active_orders_cc.filter(RQLQuery(product__id="PRD-1")).iterate()

        new_order = order_collection.create(order_data)

    """

    async def fetch_page(self, limit: int = 100, offset: int = 0) -> Collection[ModelClass]:
        """Fetch one page of resources."""
        response = await self._fetch_page_as_response(limit=limit, offset=offset)
        return self._create_collection(response)

    async def fetch_one(self) -> Model:
        """Fetch one page, expect exactly one result.

        Returns:
            One resource.

        Raises:
            ValueError: If the total matching records are not exactly one.
        """
        response = await self._fetch_page_as_response(limit=1, offset=0)
        resource_list = self._create_collection(response)
        total_records = len(resource_list)
        if resource_list.meta:
            total_records = resource_list.meta.pagination.total
        if total_records == 0:
            raise ValueError("Expected one result, but got zero results")
        if total_records > 1:
            raise ValueError(f"Expected one result, but got {total_records} results")

        return resource_list[0]

    async def iterate(self, batch_size: int = 100) -> AsyncIterator[Model]:
        """Iterate over all resources, yielding GenericResource objects.

        Args:
            batch_size: Number of resources to fetch per request

        Returns:
            Iterator of resources.
        """
        offset = 0
        limit = batch_size  # Default page size

        while True:
            response = await self._fetch_page_as_response(limit=limit, offset=offset)
            items_collection = self._create_collection(response)
            for resource in items_collection:
                yield resource

            if not items_collection.meta:
                break
            if not items_collection.meta.pagination.has_next():
                break
            offset = items_collection.meta.pagination.next_offset()

    async def create(self, resource_data: dict[str, Any]) -> Model:
        """Create a new resource using `POST /endpoint`.

        Returns:
            New resource created.
        """
        response = await self.http_client.post(self._endpoint, json=resource_data)
        response.raise_for_status()

        return self._model_class.from_response(response)

    async def get(self, resource_id: str) -> ModelClass:
        """Fetch a specific resource using `GET /endpoint/{resource_id}`."""
        return await self._resource_action(resource_id=resource_id)

    async def update(self, resource_id: str, resource_data: ResourceData) -> ModelClass:
        """Update a resource using `PUT /endpoint/{resource_id}`."""
        return await self._resource_action(resource_id, "PUT", json=resource_data)

    async def delete(self, resource_id: str) -> None:
        """Create a new resource using `POST /endpoint`.

        Returns:
            New resource created.
        """
        url = f"{self._endpoint}/{resource_id}"
        response = await self.http_client.delete(url)
        response.raise_for_status()

    async def _fetch_page_as_response(self, limit: int = 100, offset: int = 0) -> httpx.Response:
        """Fetch one page of resources.

        Returns:
            httpx.Response object.

        Raises:
            HTTPStatusError: if the response status code is not 200.
        """
        pagination_params: dict[str, int] = {"limit": limit, "offset": offset}
        response = await self.http_client.get(self.build_url(pagination_params))
        response.raise_for_status()

        return response

    async def _resource_do_request(
        self,
        resource_id: str,
        method: str = "GET",
        action: str | None = None,
        json: ResourceData | ResourceList | None = None,
    ) -> httpx.Response:
        """Perform an action on a specific resource using.

        Request with action: `HTTP_METHOD /endpoint/{resource_id}/{action}`.
        Request without action: `HTTP_METHOD /endpoint/{resource_id}`.

        Args:
            resource_id: The resource ID to operate on.
            method: The HTTP method to use.
            action: The action name to use.
            json: The updated resource data.

        Raises:
            HTTPError: If the action fails.
        """
        resource_url = f"{self._endpoint}/{resource_id}"
        url = f"{resource_url}/{action}" if action else resource_url
        response = await self.http_client.request(method, url, json=json)
        response.raise_for_status()
        return response

    async def _resource_action(
        self,
        resource_id: str,
        method: str = "GET",
        action: str | None = None,
        json: ResourceData | ResourceList | None = None,
    ) -> ModelClass:
        """Perform an action on a specific resource using `HTTP_METHOD /endpoint/{resource_id}`."""
        response = await self._resource_do_request(resource_id, method, action, json=json)
        return self._model_class.from_response(response)
