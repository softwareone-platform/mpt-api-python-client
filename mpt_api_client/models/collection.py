from collections.abc import Iterator
from typing import Any, ClassVar, Self, override

from httpx import Response

from mpt_api_client.models.base import BaseCollection, ResourceData
from mpt_api_client.models.meta import Meta
from mpt_api_client.models.resource import Resource


class Collection[ResourceType](BaseCollection):
    """Provides a base collection to interact with api collection data using fluent interfaces."""

    _data_key: ClassVar[str] = "data"
    _resource_model: type[Resource] = Resource

    def __init__(
        self, collection_data: list[ResourceData] | None = None, meta: Meta | None = None
    ) -> None:
        self.meta = meta
        collection_data = collection_data or []
        self._resource_collection = [
            self._resource_model.new(resource_data, meta) for resource_data in collection_data
        ]

    def __getitem__(self, index: int) -> ResourceType:
        """Returns the collection item at the given index."""
        return self._resource_collection[index]  # type: ignore[return-value]

    def __iter__(self) -> Iterator[ResourceType]:
        """Make GenericCollection iterable."""
        return iter(self._resource_collection)  # type: ignore[arg-type]

    def __len__(self) -> int:
        """Return the number of items in the collection."""
        return len(self._resource_collection)

    def __bool__(self) -> bool:
        """Returns True if collection has items."""
        return len(self._resource_collection) > 0

    @override
    @classmethod
    def from_response(cls, response: Response) -> Self:
        response_data = response.json().get(cls._data_key)
        meta = Meta.from_response(response)
        if not isinstance(response_data, list):
            raise TypeError(f"Response `{cls._data_key}` must be a list for collection endpoints.")

        return cls(response_data, meta)

    @override
    def to_list(self) -> list[dict[str, Any]]:
        return [resource.to_dict() for resource in self._resource_collection]
