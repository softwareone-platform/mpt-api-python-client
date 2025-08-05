import math
from dataclasses import dataclass, field
from typing import Any, ClassVar, Self, override

from box import Box
from httpx import Response


@dataclass
class Pagination:
    """Provides pagination information."""

    limit: int = 0
    offset: int = 0
    total: int = 0

    def has_next(self) -> bool:
        """Returns True if there is a next page."""
        return self.num_page() + 1 < self.total_pages()

    def num_page(self) -> int:
        """Returns the current page number starting the first page as 0."""
        if self.limit == 0:
            return 0
        return self.offset // self.limit

    def total_pages(self) -> int:
        """Returns the total number of pages."""
        if self.limit == 0:
            return 0
        return math.ceil(self.total / self.limit)

    def next_offset(self) -> int:
        """Returns the next offset as an integer for the next page."""
        return self.offset + self.limit


@dataclass
class Meta:
    """Provides meta-information about the pagination, ignored fields and the response."""

    response: Response
    pagination: Pagination = field(default_factory=Pagination)
    ignored: list[str] = field(default_factory=list)

    @classmethod
    def from_response(cls, response: Response) -> Self:
        """Creates a meta object from response."""
        meta_data = response.json().get("$meta", {})
        if not isinstance(meta_data, dict):
            raise TypeError("Response $meta must be a dict.")

        return cls(
            ignored=meta_data.get("ignored", []),
            pagination=Pagination(**meta_data.get("pagination", {})),
            response=response,
        )


ResourceData = dict[str, Any]


class GenericResource:
    """Provides a base resource to interact with api data using fluent interfaces."""

    _data_key: ClassVar[str] = "data"
    _safe_attributes: ClassVar[list[str]] = ["meta", "_resource_data"]

    def __init__(self, resource_data: ResourceData | None = None, meta: Meta | None = None) -> None:
        self.meta = meta
        self._resource_data = Box(resource_data or {}, camel_killer_box=True, default_box=False)

    def __getattr__(self, attribute: str) -> Box | Any:
        """Returns the resource data."""
        return self._resource_data.__getattr__(attribute)  # type: ignore[no-untyped-call]

    @override
    def __setattr__(self, attribute: str, attribute_value: Any) -> None:
        """Sets the resource data."""
        if attribute in self._safe_attributes:
            object.__setattr__(self, attribute, attribute_value)
            return

        self._resource_data.__setattr__(attribute, attribute_value)  # type: ignore[no-untyped-call]

    @classmethod
    def from_response(cls, response: Response) -> Self:
        """Creates a resource from a response.

        Expected a Response with json data with two keys: data and $meta.
        """
        response_data = response.json().get(cls._data_key)
        if not isinstance(response_data, dict):
            raise TypeError("Response data must be a dict.")
        meta = Meta.from_response(response)
        return cls(response_data, meta)

    def to_dict(self) -> dict[str, Any]:
        """Returns the resource as a dictionary."""
        return self._resource_data.to_dict()
