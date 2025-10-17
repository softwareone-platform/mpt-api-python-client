import json
from collections.abc import AsyncIterator, Iterator
from typing import Self
from urllib.parse import urljoin

from mpt_api_client.http.query_state import QueryState
from mpt_api_client.http.types import FileTypes, Response
from mpt_api_client.models import Collection, FileModel, ResourceData
from mpt_api_client.models import Model as BaseModel
from mpt_api_client.rql import RQLQuery


def _json_to_file_payload(resource_data: ResourceData) -> bytes:
    return json.dumps(
        resource_data, ensure_ascii=False, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


class CreateMixin[Model]:
    """Create resource mixin."""

    def create(self, resource_data: ResourceData) -> Model:
        """Create a new resource using `POST /endpoint`.

        Returns:
            New resource created.
        """
        response = self.http_client.request("post", self.path, json=resource_data)  # type: ignore[attr-defined]

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class DeleteMixin:
    """Delete resource mixin."""

    def delete(self, resource_id: str) -> None:
        """Delete resource using `DELETE /endpoint/{resource_id}`.

        Args:
            resource_id: Resource ID.
        """
        self._resource_do_request(resource_id, "DELETE")  # type: ignore[attr-defined]


class UpdateMixin[Model]:
    """Update resource mixin."""

    def update(self, resource_id: str, resource_data: ResourceData) -> Model:
        """Update a resource using `PUT /endpoint/{resource_id}`.

        Args:
            resource_id: Resource ID.
            resource_data: Resource data.

        Returns:
            Resource object.

        """
        return self._resource_action(resource_id, "PUT", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class FileOperationsMixin[Model]:
    """Mixin that provides create and download methods for file-based resources."""

    def create(
        self,
        resource_data: ResourceData | None = None,
        files: dict[str, FileTypes] | None = None,  # noqa: WPS221
        data_key: str = "_attachment_data",
    ) -> Model:
        """Create resource with file support.

        Args:
            resource_data: Resource data.
            files: Files data.
            data_key: Key to use for the JSON data in the multipart form.

        Returns:
            Created resource.
        """
        files = files or {}

        if resource_data:
            files[data_key] = (
                None,
                _json_to_file_payload(resource_data),
                "application/json",
            )

        response = self.http_client.request("post", self.path, files=files)  # type: ignore[attr-defined]

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]

    def download(self, resource_id: str) -> FileModel:
        """Download the file for the given resource ID.

        Args:
            resource_id: Resource ID.

        Returns:
            File model containing the downloaded file.
        """
        response: Response = self._resource_do_request(  # type: ignore[attr-defined]
            resource_id, method="GET", headers={"Accept": "*"}
        )
        return FileModel(response)


class AsyncCreateMixin[Model]:
    """Create resource mixin."""

    async def create(self, resource_data: ResourceData) -> Model:
        """Create a new resource using `POST /endpoint`.

        Returns:
            New resource created.
        """
        response = await self.http_client.request("post", self.path, json=resource_data)  # type: ignore[attr-defined]

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class AsyncDeleteMixin:
    """Delete resource mixin."""

    async def delete(self, resource_id: str) -> None:
        """Delete resource using `DELETE /endpoint/{resource_id}`.

        Args:
            resource_id: Resource ID.
        """
        url = urljoin(f"{self.path}/", resource_id)  # type: ignore[attr-defined]
        await self.http_client.request("delete", url)  # type: ignore[attr-defined]


class AsyncUpdateMixin[Model]:
    """Update resource mixin."""

    async def update(self, resource_id: str, resource_data: ResourceData) -> Model:
        """Update a resource using `PUT /endpoint/{resource_id}`.

        Args:
            resource_id: Resource ID.
            resource_data: Resource data.

        Returns:
            Resource object.

        """
        return await self._resource_action(resource_id, "PUT", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class AsyncFileOperationsMixin[Model]:
    """Async mixin that provides create and download methods for file-based resources."""

    async def create(
        self,
        resource_data: ResourceData | None = None,
        files: dict[str, FileTypes] | None = None,  # noqa: WPS221
        data_key: str = "_attachment_data",
    ) -> Model:
        """Create resource with file support.

        Args:
            resource_data: Resource data.
            files: Files data.
            data_key: Key to use for the JSON data in the multipart form.

        Returns:
            Created resource.
        """
        files = files or {}

        if resource_data:
            files[data_key] = (
                None,
                _json_to_file_payload(resource_data),
                "application/json",
            )

        response = await self.http_client.request("post", self.path, files=files)  # type: ignore[attr-defined]

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]

    async def download(self, resource_id: str) -> FileModel:
        """Download the file for the given resource ID.

        Args:
            resource_id: Resource ID.

        Returns:
            File model containing the downloaded file.
        """
        response = await self._resource_do_request(  # type: ignore[attr-defined]
            resource_id, method="GET", headers={"Accept": "*"}
        )
        return FileModel(response)


class GetMixin[Model]:
    """Get resource mixin."""

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

        return self._resource_action(resource_id=resource_id, query_params={"select": select})  # type: ignore[attr-defined, no-any-return]


class AsyncGetMixin[Model]:
    """Async get resource mixin."""

    async def get(self, resource_id: str, select: list[str] | str | None = None) -> Model:
        """Fetch a specific resource using `GET /endpoint/{resource_id}`.

        Args:
            resource_id: Resource ID.
            select: List of fields to select.

        Returns:
            Resource object.
        """
        if isinstance(select, list):
            select = ",".join(select) if select else None
        return await self._resource_action(resource_id=resource_id, query_params={"select": select})  # type: ignore[attr-defined, no-any-return]


class QueryableMixin:
    """Mixin providing query functionality for filtering, ordering, and selecting fields."""

    def order_by(self, *fields: str) -> Self:
        """Returns new collection with ordering setup.

        Returns:
            New collection with ordering setup.

        Raises:
            ValueError: If ordering has already been set.
        """
        if self.query_state.order_by is not None:  # type: ignore[attr-defined]
            raise ValueError("Ordering is already set. Cannot set ordering multiple times.")
        return self._create_new_instance(
            query_state=QueryState(
                rql=self.query_state.filter,  # type: ignore[attr-defined]
                order_by=list(fields),
                select=self.query_state.select,  # type: ignore[attr-defined]
            )
        )

    def filter(self, rql: RQLQuery) -> Self:
        """Creates a new collection with the filter added to the filter collection.

        Returns:
            New copy of the collection with the filter added.
        """
        existing_filter = self.query_state.filter  # type: ignore[attr-defined]
        combined_filter = existing_filter & rql if existing_filter else rql
        return self._create_new_instance(
            QueryState(
                rql=combined_filter,
                order_by=self.query_state.order_by,  # type: ignore[attr-defined]
                select=self.query_state.select,  # type: ignore[attr-defined]
            )
        )

    def select(self, *fields: str) -> Self:
        """Set select fields. Raises ValueError if select fields are already set.

        Returns:
            New copy of the collection with the select fields set.

        Raises:
            ValueError: If select fields are already set.
        """
        if self.query_state.select is not None:  # type: ignore[attr-defined]
            raise ValueError(
                "Select fields are already set. Cannot set select fields multiple times."
            )
        return self._create_new_instance(
            QueryState(
                rql=self.query_state.filter,  # type: ignore[attr-defined]
                order_by=self.query_state.order_by,  # type: ignore[attr-defined]
                select=list(fields),
            ),
        )

    def _create_new_instance(
        self,
        query_state: QueryState,
    ) -> Self:
        """Create a new instance with the given parameters."""
        return self.__class__(
            http_client=self.http_client,  # type: ignore[call-arg,attr-defined]
            query_state=query_state,
            endpoint_params=self.endpoint_params,  # type: ignore[attr-defined]
        )


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


class ModifiableResourceMixin[Model](GetMixin[Model], UpdateMixin[Model], DeleteMixin):
    """Editable resource mixin allows to read and update a resource resources."""


class AsyncModifiableResourceMixin[Model](
    AsyncGetMixin[Model], AsyncUpdateMixin[Model], AsyncDeleteMixin
):
    """Editable resource mixin allows to read and update a resource resources."""


class ManagedResourceMixin[Model](CreateMixin[Model], ModifiableResourceMixin[Model]):
    """Managed resource mixin allows to read, create, update and delete a resource resources."""


class AsyncManagedResourceMixin[Model](
    AsyncCreateMixin[Model], AsyncModifiableResourceMixin[Model]
):
    """Managed resource mixin allows to read, create, update and delete a resource resources."""
