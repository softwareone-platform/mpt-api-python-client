from abc import ABC
from typing import Any, ClassVar, Self, override
from urllib.parse import urljoin

from httpx import Response

from mpt_api_client.http.client import HTTPClient, HTTPClientAsync
from mpt_api_client.models import Resource
from mpt_api_client.models.base import ResourceData, ResourceList


class ResourceMixin:
    """Mixin for resource clients."""

    _endpoint: str
    _resource_class: type[Any]
    _safe_attributes: ClassVar[set[str]] = {"http_client_", "resource_id_", "resource_"}

    def __init__(
        self, http_client: HTTPClient | HTTPClientAsync, resource_id: str, resource: Resource | None
    ) -> None:
        self.http_client_ = http_client
        self.resource_id_ = resource_id
        self.resource_: Resource | None = resource

    def __getattr__(self, attribute: str) -> Any:
        """Returns the resource data."""
        self._assert_resource_is_set()
        return self.resource_.__getattr__(attribute)  # type: ignore[union-attr]

    @property
    def resource_url(self) -> str:
        """Returns the resource URL."""
        return f"{self._endpoint}/{self.resource_id_}"

    @override
    def __setattr__(self, attribute: str, attribute_value: Any) -> None:
        if attribute in self._safe_attributes:
            object.__setattr__(self, attribute, attribute_value)
            return
        self._assert_resource_is_set()
        self.resource_.__setattr__(attribute, attribute_value)

    def _assert_resource_is_set(self) -> None:
        if not self.resource_:
            class_name = self._resource_class.__name__
            raise RuntimeError(
                f"Resource data not available. Call fetch() method first to retrieve"
                f" the resource `{class_name}`"
            )


class ResourceBaseClient[ResourceModel: Resource](ABC, ResourceMixin):
    """Client for RESTful resources."""

    _endpoint: str
    _resource_class: type[ResourceModel]
    _safe_attributes: ClassVar[set[str]] = {"http_client_", "resource_id_", "resource_"}

    def __init__(
        self, http_client: HTTPClient, resource_id: str, resource: Resource | None = None
    ) -> None:
        self.http_client_: HTTPClient = http_client  # type: ignore[mutable-override]
        ResourceMixin.__init__(
            self, http_client=http_client, resource_id=resource_id, resource=resource
        )

    def fetch(self) -> ResourceModel:
        """Fetch a specific resource using `GET /endpoint/{resource_id}`.

        It fetches and caches the resource.

        Returns:
            The fetched resource.
        """
        response = self._do_action("GET")

        self.resource_ = self._resource_class.from_response(response)
        return self.resource_

    def update(self, resource_data: ResourceData) -> ResourceModel:
        """Update a specific in the API and catches the result as a current resource.

        Args:
            resource_data: The updated resource data.

        Returns:
            The updated resource.

        Examples:
            updated_contact = contact.update({"name": "New Name"})


        """
        response = self._do_action("PUT", json=resource_data)
        self.resource_ = self._resource_class.from_response(response)
        return self.resource_

    def save(self) -> Self:
        """Save the current state of the resource to the api using the update method.

        Raises:
            ValueError: If the resource has not been set.

        Examples:
            contact.name = "New Name"
            contact.save()

        """
        self._assert_resource_is_set()
        self.update(self.resource_.to_dict())  # type: ignore[union-attr]
        return self

    def delete(self) -> None:
        """Delete the resource using `DELETE /endpoint/{resource_id}`.

        Raises:
            HTTPStatusError: If the deletion fails.

        Examples:
            contact.delete()
        """
        response = self._do_action("DELETE")
        response.raise_for_status()

        self.resource_ = None

    def _resource_action(
        self,
        method: str = "GET",
        url: str | None = None,
        json: ResourceData | ResourceList | None = None,
    ) -> ResourceModel:
        """Perform an action on a specific resource using `HTTP_METHOD /endpoint/{resource_id}`."""
        response = self._do_action(method, url, json=json)
        self.resource_ = self._resource_class.from_response(response)
        return self.resource_

    def _do_action(
        self,
        method: str = "GET",
        url: str | None = None,
        json: ResourceData | ResourceList | None = None,
    ) -> Response:
        """Perform an action on a specific resource using `HTTP_METHOD /endpoint/{resource_id}`.

        Args:
            method: The HTTP method to use.
            url: The action name to use.
            json: The updated resource data.

        Raises:
            HTTPError: If the action fails.
        """
        url = f"{self.resource_url}/{url}" if url else self.resource_url
        response = self.http_client_.request(method, url, json=json)
        response.raise_for_status()
        return response


class AsyncResourceBaseClient[ResourceModel: Resource](ABC, ResourceMixin):
    """Client for RESTful resources."""

    _endpoint: str
    _resource_class: type[ResourceModel]
    _safe_attributes: ClassVar[set[str]] = {"http_client_", "resource_id_", "resource_"}

    def __init__(
        self, http_client: HTTPClientAsync, resource_id: str, resource: Resource | None = None
    ) -> None:
        self.http_client_: HTTPClientAsync = http_client  # type: ignore[mutable-override]
        ResourceMixin.__init__(
            self, http_client=http_client, resource_id=resource_id, resource=resource
        )

    async def fetch(self) -> ResourceModel:
        """Fetch a specific resource using `GET /endpoint/{resource_id}`.

        It fetches and caches the resource.

        Returns:
            The fetched resource.
        """
        response = await self._do_action("GET")

        self.resource_ = self._resource_class.from_response(response)
        return self.resource_

    async def update(self, resource_data: ResourceData) -> ResourceModel:
        """Update a specific in the API and catches the result as a current resource.

        Args:
            resource_data: The updated resource data.

        Returns:
            The updated resource.

        Examples:
            updated_contact = contact.update({"name": "New Name"})


        """
        return await self._resource_action("PUT", json=resource_data)

    async def save(self) -> Self:
        """Save the current state of the resource to the api using the update method.

        Raises:
            ValueError: If the resource has not been set.

        Examples:
            contact.name = "New Name"
            contact.save()

        """
        self._assert_resource_is_set()
        await self.update(self.resource_.to_dict())  # type: ignore[union-attr]
        return self

    async def delete(self) -> None:
        """Delete the resource using `DELETE /endpoint/{resource_id}`.

        Raises:
            HTTPStatusError: If the deletion fails.

        Examples:
            contact.delete()
        """
        response = await self._do_action("DELETE")
        response.raise_for_status()

        self.resource_ = None

    async def _resource_action(
        self,
        method: str = "GET",
        url: str | None = None,
        json: ResourceData | ResourceList | None = None,
    ) -> ResourceModel:
        """Perform an action on a specific resource using `HTTP_METHOD /endpoint/{resource_id}`."""
        response = await self._do_action(method, url, json=json)
        self.resource_ = self._resource_class.from_response(response)
        return self.resource_

    async def _do_action(
        self,
        method: str = "GET",
        url: str | None = None,
        json: ResourceData | ResourceList | None = None,
    ) -> Response:
        """Perform an action on a specific resource using `HTTP_METHOD /endpoint/{resource_id}`.

        Args:
            method: The HTTP method to use.
            url: The action name to use.
            json: The updated resource data.

        Raises:
            HTTPError: If the action fails.
        """
        url = urljoin(self.resource_url, url) if url else self.resource_url
        response = await self.http_client_.request(method, url, json=json)
        response.raise_for_status()
        return response
