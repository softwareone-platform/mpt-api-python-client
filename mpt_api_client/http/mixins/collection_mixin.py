from collections.abc import AsyncIterator, Iterator

from mpt_api_client.http.mixins.queryable_mixin import QueryableMixin
from mpt_api_client.http.types import Response
from mpt_api_client.models import Collection
from mpt_api_client.models import Model as BaseModel


class CollectionMixin[Model: BaseModel](QueryableMixin):
    """Mixin providing collection functionality."""

    def fetch_page(self, limit: int = 100, offset: int = 0) -> Collection[Model]:
        """Fetch one page of resources.

        Returns:
            Collection of resources.
        """
        response = self._fetch_page_as_response(limit=limit, offset=offset)
        return self.make_collection(response)  # type: ignore[attr-defined, no-any-return]

    def fetch_one(self) -> Model:
        """Fetch one resource, expect exactly one result.

        Returns:
            One resource.

        Raises:
            ValueError: If the total matching records are not exactly one.
        """
        response = self._fetch_page_as_response(limit=1, offset=0)
        resource_list = self.make_collection(response)  # type: ignore[attr-defined]
        total_records = len(resource_list)
        if resource_list.meta:
            total_records = resource_list.meta.pagination.total
        if total_records == 0:
            raise ValueError("Expected one result, but got zero results")
        if total_records > 1:
            raise ValueError(f"Expected one result, but got {total_records} results")

        return resource_list[0]  # type: ignore[no-any-return]

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
            items_collection = self.make_collection(response)  # type: ignore[attr-defined]
            yield from items_collection

            if not items_collection.meta:
                break
            if not items_collection.meta.pagination.has_next():
                break
            offset = items_collection.meta.pagination.next_offset()

    def _fetch_page_as_response(self, limit: int = 100, offset: int = 0) -> Response:
        """Fetch one page of resources.

        Returns:
            Response object.

        Raises:
            HTTPStatusError: if the response status code is not 200.
        """
        pagination_params: dict[str, int] = {"limit": limit, "offset": offset}
        return self.http_client.request("get", self.build_path(pagination_params))  # type: ignore[attr-defined, no-any-return]


class AsyncCollectionMixin[Model: BaseModel](QueryableMixin):
    """Async mixin providing collection functionality."""

    async def fetch_page(self, limit: int = 100, offset: int = 0) -> Collection[Model]:
        """Fetch one page of resources.

        Returns:
            Collection of resources.
        """
        response = await self._fetch_page_as_response(limit=limit, offset=offset)
        return self.make_collection(response)  # type: ignore[no-any-return,attr-defined]

    async def fetch_one(self) -> Model:
        """Fetch one resource, expect exactly one result.

        Returns:
            One resource.

        Raises:
            ValueError: If the total matching records are not exactly one.
        """
        response = await self._fetch_page_as_response(limit=1, offset=0)
        resource_list = self.make_collection(response)  # type: ignore[attr-defined]
        total_records = len(resource_list)
        if resource_list.meta:
            total_records = resource_list.meta.pagination.total
        if total_records == 0:
            raise ValueError("Expected one result, but got zero results")
        if total_records > 1:
            raise ValueError(f"Expected one result, but got {total_records} results")

        return resource_list[0]  # type: ignore[no-any-return]

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
            items_collection = self.make_collection(response)  # type: ignore[attr-defined]
            for resource in items_collection:
                yield resource

            if not items_collection.meta:
                break
            if not items_collection.meta.pagination.has_next():
                break
            offset = items_collection.meta.pagination.next_offset()

    async def _fetch_page_as_response(self, limit: int = 100, offset: int = 0) -> Response:
        """Fetch one page of resources.

        Returns:
            Response object.

        Raises:
            HTTPStatusError: if the response status code is not 200.
        """
        pagination_params: dict[str, int] = {"limit": limit, "offset": offset}
        return await self.http_client.request("get", self.build_path(pagination_params))  # type: ignore[attr-defined,no-any-return]
