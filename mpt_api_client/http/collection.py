import copy
from abc import ABC
from collections.abc import Iterator
from typing import Any, Self

import httpx

from mpt_api_client.http.client import MPTClient
from mpt_api_client.models import Collection, Resource
from mpt_api_client.rql.query_builder import RQLQuery


class CollectionBaseClient[ResourceType: Resource](ABC):  # noqa: WPS214
    """Immutable Base client for RESTful resource collections.

    Examples:
        active_orders_cc = order_collection.filter(RQLQuery(status="active"))
        active_orders = active_orders_cc.order_by("created").iterate()
        product_active_orders = active_orders_cc.filter(RQLQuery(product__id="PRD-1")).iterate()

        new_order = order_collection.create(order_data)

    """

    _endpoint: str
    _resource_class: type[ResourceType]
    _collection_class: type[Collection[ResourceType]]

    def __init__(
        self,
        query_rql: RQLQuery | None = None,
        client: MPTClient | None = None,
    ) -> None:
        self.mpt_client = client or MPTClient()
        self.query_rql: RQLQuery | None = query_rql
        self.query_order_by: list[str] | None = None
        self.query_select: list[str] | None = None

    @classmethod
    def clone(cls, collection_client: "CollectionBaseClient[ResourceType]") -> Self:
        """Create a copy of collection client for immutable operations.

        Returns:
            New collection client with same settings.
        """
        new_collection = cls(
            client=collection_client.mpt_client,
            query_rql=collection_client.query_rql,
        )
        new_collection.query_order_by = (
            copy.copy(collection_client.query_order_by)
            if collection_client.query_order_by
            else None
        )
        new_collection.query_select = (
            copy.copy(collection_client.query_select) if collection_client.query_select else None
        )
        return new_collection

    def build_url(self, query_params: dict[str, Any] | None = None) -> str:
        """Builds the endpoint URL with all the query parameters.

        Returns:
            Partial URL with query parameters.
        """
        query_params = query_params or {}
        query_parts = [
            f"{param_key}={param_value}" for param_key, param_value in query_params.items()
        ]  # noqa: WPS237
        if self.query_order_by:
            query_parts.append(f"order={','.join(self.query_order_by)}")  # noqa: WPS237
        if self.query_select:
            query_parts.append(f"select={','.join(self.query_select)}")  # noqa: WPS237
        if self.query_rql:
            query_parts.append(str(self.query_rql))
        if query_parts:
            return f"{self._endpoint}?{'&'.join(query_parts)}"  # noqa: WPS237
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
        new_collection = self.clone(self)
        new_collection.query_order_by = list(fields)
        return new_collection

    def filter(self, rql: RQLQuery) -> Self:
        """Creates a new collection with the filter added to the filter collection.

        Returns:
            New copy of the collection with the filter added.
        """
        if self.query_rql:
            rql = self.query_rql & rql
        new_collection = self.clone(self)
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

        new_client = self.clone(self)
        new_client.query_select = list(fields)
        return new_client

    def fetch_page(self, limit: int = 100, offset: int = 0) -> Collection[ResourceType]:
        """Fetch one page of resources.

        Returns:
            Collection of resources.
        """
        response = self._fetch_page_as_response(limit=limit, offset=offset)
        return Collection.from_response(response)

    def fetch_one(self) -> ResourceType:
        """Fetch one page, expect exactly one result.

        Returns:
            One resource.

        Raises:
            ValueError: If the total matching records are not exactly one.
        """
        response = self._fetch_page_as_response(limit=1, offset=0)
        resource_list: Collection[ResourceType] = Collection.from_response(response)
        total_records = len(resource_list)
        if resource_list.meta:
            total_records = resource_list.meta.pagination.total
        if total_records == 0:
            raise ValueError("Expected one result, but got zero results")
        if total_records > 1:
            raise ValueError(f"Expected one result, but got {total_records} results")

        return resource_list[0]

    def iterate(self) -> Iterator[ResourceType]:
        """Iterate over all resources, yielding GenericResource objects.

        Returns:
            Iterator of resources.
        """
        offset = 0
        limit = 100  # Default page size

        while True:
            response = self._fetch_page_as_response(limit=limit, offset=offset)
            items_collection: Collection[ResourceType] = Collection.from_response(response)
            yield from items_collection

            if not items_collection.meta:
                break
            if not items_collection.meta.pagination.has_next():
                break
            offset = items_collection.meta.pagination.next_offset()

    def create(self, resource_data: dict[str, Any]) -> ResourceType:
        """Create a new resource using `POST /endpoint`.

        Returns:
            New resource created.
        """
        response = self.mpt_client.post(self._endpoint, json=resource_data)
        response.raise_for_status()

        return self._resource_class.from_response(response)

    def _fetch_page_as_response(self, limit: int = 100, offset: int = 0) -> httpx.Response:
        """Fetch one page of resources.

        Returns:
            httpx.Response object.

        Raises:
            HTTPStatusError: if the response status code is not 200.
        """
        pagination_params: dict[str, int] = {"limit": limit, "offset": offset}
        response = self.mpt_client.get(self.build_url(pagination_params))
        response.raise_for_status()

        return response
