import math
from dataclasses import dataclass, field
from typing import Self

from mpt_api_client.http.types import Response


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
