from collections.abc import Iterator

from mpt_api_client.models.meta import Meta
from mpt_api_client.models.model import Model, ResourceData

ResourceList = list[ResourceData]


class Collection[ItemType: Model]:
    """Provides a collection to interact with api collection data using fluent interfaces."""

    def __init__(self, resources: list[ItemType] | None = None, meta: Meta | None = None) -> None:
        self.meta = meta
        self.resources = resources or []

    def __getitem__(self, index: int) -> ItemType:
        """Returns the collection item at the given index."""
        return self.resources[index]

    def __iter__(self) -> Iterator[ItemType]:
        """Make GenericCollection iterable."""
        return iter(self.resources)

    def __len__(self) -> int:
        """Return the number of items in the collection."""
        return len(self.resources)

    def __bool__(self) -> bool:
        """Returns True if collection has items."""
        return len(self.resources) > 0

    def to_list(self) -> ResourceList:
        """Returns the collection as a list of dictionaries."""
        return [resource.to_dict() for resource in self.resources]
