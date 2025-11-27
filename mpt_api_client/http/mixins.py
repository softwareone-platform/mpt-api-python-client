from collections.abc import AsyncIterator, Iterator
from typing import Self
from urllib.parse import urljoin

from mpt_api_client.constants import APPLICATION_JSON
from mpt_api_client.exceptions import MPTError
from mpt_api_client.http.client import json_to_file_payload
from mpt_api_client.http.query_state import QueryState
from mpt_api_client.http.types import FileTypes, Response
from mpt_api_client.models import Collection, FileModel, ResourceData
from mpt_api_client.models import Model as BaseModel
from mpt_api_client.rql import RQLQuery


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


class DownloadFileMixin[Model]:
    """Download file mixin."""

    def download(self, resource_id: str, accept: str | None = None) -> FileModel:
        """Download the file for the given resource ID.

        Args:
            resource_id: Resource ID.
            accept: The content type expected for the file.
                If not provided, the content type will be fetched from the resource.

        Returns:
            File model containing the downloaded file.
        """
        if not accept:
            resource: Model = self._resource_action(resource_id, method="GET")  # type: ignore[attr-defined]
            accept = resource.content_type  # type: ignore[attr-defined]
            if not accept:
                raise MPTError("Unable to download file. Content type not found in resource")
        response: Response = self._resource_do_request(  # type: ignore[attr-defined]
            resource_id, method="GET", headers={"Accept": accept}
        )
        return FileModel(response)


class FilesOperationsMixin[Model](DownloadFileMixin[Model]):
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
                json_to_file_payload(resource_data),
                APPLICATION_JSON,
            )
        response = self.http_client.request("post", self.path, files=files)  # type: ignore[attr-defined]

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class CreateFileMixin[Model]:
    """Create file mixin."""

    def create(self, resource_data: ResourceData, file: FileTypes | None = None) -> Model:  # noqa: WPS110
        """Create logo.

        Create a file resource by specifying a file image.

        Args:
            resource_data: Resource data.
            file: File image.

        Returns:
            Model: Created resource.
        """
        files = {}

        if file:
            files[self._upload_file_key] = file  # type: ignore[attr-defined]

        response = self.http_client.request(  # type: ignore[attr-defined]
            "post",
            self.path,  # type: ignore[attr-defined]
            json=resource_data,
            files=files,
            json_file_key=self._upload_data_key,  # type: ignore[attr-defined]
            force_multipart=True,
        )

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class UpdateFileMixin[Model]:
    """Update file mixin."""

    def update(
        self,
        resource_id: str,
        resource_data: ResourceData,
        file: FileTypes | None = None,  # noqa: WPS110
    ) -> Model:
        """Update file.

        Update a file resource by specifying a file.

        Args:
            resource_id: Resource ID.
            resource_data: Resource data.
            file: File image.

        Returns:
            Model: Updated resource.
        """
        files = {}

        url = urljoin(f"{self.path}/", resource_id)  # type: ignore[attr-defined]

        if file:
            files[self._upload_file_key] = file  # type: ignore[attr-defined]

        response = self.http_client.request(  # type: ignore[attr-defined]
            "put",
            url,
            json=resource_data,
            files=files,
            json_file_key=self._upload_data_key,  # type: ignore[attr-defined]
            force_multipart=True,
        )

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class AsyncCreateFileMixin[Model]:
    """Asynchronous Create file mixin."""

    async def create(self, resource_data: ResourceData, file: FileTypes | None = None) -> Model:  # noqa: WPS110
        """Create file.

        Create a file resource by specifying a file.

        Args:
            resource_data: Resource data.
            file: File image.

        Returns:
            Model: Created resource.
        """
        files = {}

        if file:
            files[self._upload_file_key] = file  # type: ignore[attr-defined]

        response = await self.http_client.request(  # type: ignore[attr-defined]
            "post",
            self.path,  # type: ignore[attr-defined]
            json=resource_data,
            files=files,
            json_file_key=self._upload_data_key,  # type: ignore[attr-defined]
            force_multipart=True,
        )

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class AsyncUpdateFileMixin[Model]:
    """Asynchronous Update file mixin."""

    async def update(
        self,
        resource_id: str,
        resource_data: ResourceData,
        file: FileTypes | None = None,  # noqa: WPS110
    ) -> Model:
        """Update file.

        Update a file resource by specifying a file.

        Args:
            resource_id: Resource ID.
            resource_data: Resource data.
            file: File image.

        Returns:
            Model: Updated resource.
        """
        files = {}

        url = urljoin(f"{self.path}/", resource_id)  # type: ignore[attr-defined]

        if file:
            files[self._upload_file_key] = file  # type: ignore[attr-defined]

        response = await self.http_client.request(  # type: ignore[attr-defined]
            "put",
            url,
            json=resource_data,
            files=files,
            json_file_key=self._upload_data_key,  # type: ignore[attr-defined]
            force_multipart=True,
        )

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


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


class AsyncDownloadFileMixin[Model]:
    """Download file mixin."""

    async def download(self, resource_id: str, accept: str | None = None) -> FileModel:
        """Download the file for the given resource ID.

        Args:
            resource_id: Resource ID.
            accept: The content type expected for the file.
                If not provided, the content type will be fetched from the resource.

        Returns:
            File model containing the downloaded file.
        """
        if not accept:
            resource: Model = await self._resource_action(resource_id, method="GET")  # type: ignore[attr-defined]
            accept = resource.content_type  # type: ignore[attr-defined]
            if not accept:
                raise MPTError("Unable to download file. Content type not found in resource")
        response = await self._resource_do_request(  # type: ignore[attr-defined]
            resource_id, method="GET", headers={"Accept": accept}
        )
        return FileModel(response)


class AsyncFilesOperationsMixin[Model](AsyncDownloadFileMixin[Model]):
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
                json_to_file_payload(resource_data),
                APPLICATION_JSON,
            )

        response = await self.http_client.request("post", self.path, files=files)  # type: ignore[attr-defined]

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


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


class AsyncEnableMixin[Model: BaseModel]:
    """Enable resource mixin."""

    async def enable(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Enable a specific resource."""
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id=resource_id, method="POST", action="enable", json=resource_data
        )


class EnableMixin[Model: BaseModel]:
    """Enable resource mixin."""

    def enable(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Enable a specific resource."""
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id=resource_id, method="POST", action="enable", json=resource_data
        )


class AsyncDisableMixin[Model: BaseModel]:
    """Disable resource mixin."""

    async def disable(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Disable a specific resource."""
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id=resource_id, method="POST", action="disable", json=resource_data
        )


class DisableMixin[Model: BaseModel]:
    """Disable resource mixin."""

    def disable(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Disable a specific resource  ."""
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id=resource_id, method="POST", action="disable", json=resource_data
        )


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
