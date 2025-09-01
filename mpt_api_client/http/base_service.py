import copy
from typing import Any, Self

import httpx

from mpt_api_client.models import Collection, Meta
from mpt_api_client.models import Model as BaseModel
from mpt_api_client.rql import RQLQuery


class ServiceBase[Client, Model: BaseModel]:
    """Service base with agnostic HTTP client."""

    _endpoint: str
    _model_class: type[Model]
    _collection_key = "data"

    def __init__(
        self,
        *,
        http_client: Client,
        query_rql: RQLQuery | None = None,
        query_order_by: list[str] | None = None,
        query_select: list[str] | None = None,
    ) -> None:
        self.http_client = http_client
        self.query_rql: RQLQuery | None = query_rql
        self.query_order_by = query_order_by
        self.query_select = query_select

    def clone(self) -> Self:
        """Create a copy of collection client for immutable operations.

        Returns:
            New collection client with same settings.
        """
        return type(self)(
            http_client=self.http_client,
            query_rql=self.query_rql,
            query_order_by=copy.copy(self.query_order_by) if self.query_order_by else None,
            query_select=copy.copy(self.query_select) if self.query_select else None,
        )

    def build_url(self, query_params: dict[str, Any] | None = None) -> str:  # noqa: WPS210
        """Builds the endpoint URL with all the query parameters.

        Returns:
            Partial URL with query parameters.
        """
        query_params = query_params or {}
        query_parts = [
            f"{param_key}={param_value}" for param_key, param_value in query_params.items()
        ]
        if self.query_order_by:
            str_order_by = ",".join(self.query_order_by)
            query_parts.append(f"order={str_order_by}")
        if self.query_select:
            str_query_select = ",".join(self.query_select)
            query_parts.append(f"select={str_query_select}")
        if self.query_rql:
            query_parts.append(str(self.query_rql))
        if query_parts:
            query = "&".join(query_parts)
            return f"{self._endpoint}?{query}"
        return self._endpoint

    def order_by(self, *fields: str) -> Self:
        """Returns new collection with ordering setup.

        Returns:
            New collection with ordering setup.

        Raises:
            ValueError: If ordering has already been set.
        """
        if self.query_order_by is not None:
            raise ValueError("Ordering is already set. Cannot set ordering multiple times.")
        new_collection = self.clone()
        new_collection.query_order_by = list(fields)
        return new_collection

    def filter(self, rql: RQLQuery) -> Self:
        """Creates a new collection with the filter added to the filter collection.

        Returns:
            New copy of the collection with the filter added.
        """
        if self.query_rql:
            rql = self.query_rql & rql
        new_collection = self.clone()
        new_collection.query_rql = rql
        return new_collection

    def select(self, *fields: str) -> Self:
        """Set select fields. Raises ValueError if select fields are already set.

        Returns:
            New copy of the collection with the select fields set.

        Raises:
            ValueError: If select fields are already set.
        """
        if self.query_select is not None:
            raise ValueError(
                "Select fields are already set. Cannot set select fields multiple times."
            )

        new_client = self.clone()
        new_client.query_select = list(fields)
        return new_client

    def _create_collection(self, response: httpx.Response) -> Collection[Model]:
        meta = Meta.from_response(response)
        return Collection(
            resources=[
                self._model_class.new(resource, meta)
                for resource in response.json().get(self._collection_key)
            ],
            meta=meta,
        )
