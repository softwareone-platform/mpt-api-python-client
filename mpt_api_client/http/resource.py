from abc import ABC
from typing import Any, ClassVar, Self, override

from mpt_api_client.http.client import MPTClient
from mpt_api_client.models import Resource


class ResourceBaseClient[ResourceType: Resource](ABC):  # noqa: WPS214
    """Client for RESTful resources."""

    _endpoint: str
    _resource_class: type[Resource]
    _safe_attributes: ClassVar[set[str]] = {"mpt_client_", "resource_id_", "resource_"}

    def __init__(self, client: MPTClient, resource_id: str) -> None:
        self.mpt_client_ = client  # noqa: WPS120
        self.resource_id_ = resource_id  # noqa: WPS120
        self.resource_: Resource | None = None  # noqa: WPS120

    def __getattr__(self, attribute: str) -> Any:
        """Returns the resource data."""
        self._ensure_resource_is_fetched()
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
        self._ensure_resource_is_fetched()
        self.resource_.__setattr__(attribute, attribute_value)

    def fetch(self) -> Resource:
        """Fetch a specific resource using `GET /endpoint/{resource_id}`.

        It fetches and caches the resource.

        Returns:
            The fetched resource.
        """
        response = self.mpt_client_.get(self.resource_url)
        response.raise_for_status()

        self.resource_ = self._resource_class.from_response(response)  # noqa: WPS120
        return self.resource_

    def update(self, resource_data: dict[str, Any]) -> Resource:
        """Update a specific in the API and catches the result as a current resource.

        Args:
            resource_data: The updated resource data.

        Returns:
            The updated resource.

        Examples:
            updated_contact = contact.update({"name": "New Name"})


        """
        response = self.mpt_client_.put(self.resource_url, json=resource_data)
        response.raise_for_status()

        self.resource_ = self._resource_class.from_response(response)  # noqa: WPS120
        return self.resource_

    def save(self) -> Self:
        """Save the current state of the resource to the api using the update method.

        Raises:
            ValueError: If the resource has not been set.

        Examples:
            contact.name = "New Name"
            contact.save()

        """
        if not self.resource_:
            raise ValueError("Unable to save resource that has not been set.")
        self.update(self.resource_.to_dict())
        return self

    def delete(self) -> None:
        """Delete the resource using `DELETE /endpoint/{resource_id}`.

        Raises:
            HTTPStatusError: If the deletion fails.

        Examples:
            contact.delete()
        """
        response = self.mpt_client_.delete(self.resource_url)
        response.raise_for_status()

        self.resource_ = None  # noqa: WPS120

    def _ensure_resource_is_fetched(self) -> None:
        if not self.resource_:
            self.fetch()
