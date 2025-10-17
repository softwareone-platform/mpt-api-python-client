from typing import Any

from mpt_api_client.http.query_state import QueryState
from mpt_api_client.http.types import Response
from mpt_api_client.models import Collection, Meta
from mpt_api_client.models import Model as BaseModel


class ServiceBase[Client, Model: BaseModel]:  # noqa: WPS214
    """Service base with agnostic HTTP client."""

    _endpoint: str
    _model_class: type[Model]
    _collection_key = "data"

    def __init__(
        self,
        *,
        http_client: Client,
        query_state: QueryState | None = None,
        endpoint_params: dict[str, str] | None = None,
    ) -> None:
        self.http_client = http_client
        self.query_state = query_state or QueryState()
        self.endpoint_params = endpoint_params or {}

    @property
    def path(self) -> str:
        """Service endpoint URL."""
        return self._endpoint.format(**self.endpoint_params)

    def build_path(
        self,
        query_params: dict[str, Any] | None = None,
    ) -> str:
        """Builds the endpoint URL with all the query parameters.

        Returns:
            Complete URL with query parameters.
        """
        query = self.query_state.build(query_params)
        return f"{self.path}?{query}" if query else self.path

    @classmethod
    def make_collection(cls, response: Response) -> Collection[Model]:
        """Builds a collection from a response.

        Args:
            response: The response object.
        """
        meta = Meta.from_response(response)
        return Collection(
            resources=[
                cls._model_class.new(resource, meta)
                for resource in response.json().get(cls._collection_key)
            ],
            meta=meta,
        )
