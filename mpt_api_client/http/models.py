import math
from dataclasses import dataclass, field
from typing import Any, Self

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
        return self.offset + self.limit < self.total

    def num_page(self) -> int:
        """Returns the current page number."""
        if self.limit == 0:
            return 0
        return (self.offset // self.limit) + 1

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
    """Provides meta information about the pagination, ignored fields and the response."""

    pagination: Pagination = field(default_factory=Pagination)
    ignored: list[str] = field(default_factory=list)
    response: Response | None = None

    @classmethod
    def from_response(cls, response: Response) -> Self:
        """Creates a meta object from response."""
        meta_data = response.json().get("$meta")
        if not isinstance(meta_data, dict):
            raise TypeError("Response $meta must be a dict.")

        return cls(
            ignored=meta_data.get("ignored", []),
            pagination=Pagination(**meta_data.get("pagination", {})),
            response=response,
        )


class GenericResource(Box):
    """Provides a base resource to interact with api data using fluent interfaces."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__post_init__()

    def __post_init__(self) -> None:
        """Initializes meta information."""
        meta = self.get("$meta", None)  # type: ignore[no-untyped-call]
        if meta:
            self._meta = Meta(**meta)

    @classmethod
    def from_response(cls, response: Response) -> Self:
        """Creates a resource from a response.

        Expected a Response with json data with two keys: data and $meta.
        """
        response_data = response.json().get("data")
        if not isinstance(response_data, dict):
            raise TypeError("Response data must be a dict.")
        meta = Meta.from_response(response)
        meta.response = response
        resource = cls(response_data)
        resource._meta = meta
        return resource
