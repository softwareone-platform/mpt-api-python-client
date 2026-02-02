from typing import Self

from mpt_api_client.http.query_state import QueryState
from mpt_api_client.rql import RQLQuery


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
