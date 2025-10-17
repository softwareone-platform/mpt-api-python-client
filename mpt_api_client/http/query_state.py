from typing import Any

from mpt_api_client.rql import RQLQuery


class QueryState:
    """Stores and manages API query state for filtering, selecting, and ordering data.

    This class maintains the current state of query parameters (filter, order_by, select)
    and provides functionality to build query strings from that state. It's responsible
    for both storing query configuration and constructing the appropriate query parameters
    that modify the behavior and shape of data returned by the API.
    """

    def __init__(
        self,
        rql: RQLQuery | None = None,
        order_by: list[str] | None = None,
        select: list[str] | None = None,
    ) -> None:
        """Initialize the query state with optional filter, ordering, and selection criteria.

        Args:
            rql: RQL query for filtering data.
            order_by: List of fields to order by (prefix with '-' for descending).
            select: List of fields to select in the response.
        """
        self._filter = rql
        self._order_by = order_by
        self._select = select

    @property
    def filter(self) -> RQLQuery | None:
        """Get the current filter query."""
        return self._filter

    @property
    def order_by(self) -> list[str] | None:
        """Get the current order by fields."""
        return self._order_by

    @property
    def select(self) -> list[str] | None:
        """Get the current select fields."""
        return self._select

    def build(self, query_params: dict[str, Any] | None = None) -> str:
        """Build a query string from the current state and additional parameters.

        Args:
            query_params: Additional query parameters to include in the query string.

        Returns:
            Complete query string with all parameters, or empty string if no parameters.
        """
        query_params = query_params or {}
        if self._order_by:
            query_params.update({"order": ",".join(self._order_by)})
        if self._select:
            query_params.update({"select": ",".join(self._select)})

        query_parts = [
            f"{param_key}={param_value}" for param_key, param_value in query_params.items()
        ]

        if self._filter:
            query_parts.append(str(self._filter))

        if query_parts:
            query = "&".join(query_parts)
            return f"{query}"
        return ""
