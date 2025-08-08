from abc import ABC, abstractmethod
from typing import Any, Self

from httpx import Response

from mpt_api_client.models.meta import Meta

ResourceData = dict[str, Any]


class BaseResource(ABC):
    """Provides a base resource to interact with api data using fluent interfaces."""

    @classmethod
    @abstractmethod
    def new(cls, resource_data: ResourceData | None = None, meta: Meta | None = None) -> Self:
        """Creates a new resource from ResourceData and Meta."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_response(cls, response: Response) -> Self:
        """Creates a collection from a response.

        Args:
            response: The httpx response object.
        """
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Returns the resource as a dictionary."""
        raise NotImplementedError


class BaseCollection(ABC):
    """Provides a base collection to interact with api collection data using fluent interfaces."""

    @classmethod
    @abstractmethod
    def from_response(cls, response: Response) -> Self:
        """Creates a collection from a response.

        Args:
            response: The httpx response object.
        """
        raise NotImplementedError

    @abstractmethod
    def to_list(self) -> list[dict[str, Any]]:
        """Returns the collection as a list of dictionaries."""
        raise NotImplementedError
