import json
from collections.abc import AsyncIterator, Iterator

from mpt_api_client.constants import APPLICATION_JSONL
from mpt_api_client.http.mixins.queryable_mixin import QueryableMixin
from mpt_api_client.models import Model as BaseModel


class StreamJSONLMixin[Model: BaseModel](QueryableMixin):
    """Mixin providing JSONL (NDJSON) streaming of a collection line by line."""

    def stream(self) -> Iterator[Model]:
        """Stream resources from a JSONL endpoint, yielding one model per line.

        Unlike ``iterate()``, which paginates and deserializes full pages, this
        consumes a ``application/jsonl`` response line by line without buffering the
        whole body in memory.

        Yields:
            Resources, one per non-empty line of the response.
        """
        with self.http_client.stream(  # type: ignore[attr-defined]
            "GET",
            self.build_path(),  # type: ignore[attr-defined]
            headers={"Accept": APPLICATION_JSONL},
        ) as response:
            for line in response.iter_lines():
                if line.strip():
                    yield self._model_class(json.loads(line))  # type: ignore[attr-defined]


class AsyncStreamJSONLMixin[Model: BaseModel](QueryableMixin):
    """Async mixin providing JSONL (NDJSON) streaming of a collection line by line."""

    async def stream(self) -> AsyncIterator[Model]:
        """Stream resources from a JSONL endpoint, yielding one model per line.

        Unlike ``iterate()``, which paginates and deserializes full pages, this
        consumes a ``application/jsonl`` response line by line without buffering the
        whole body in memory.

        Yields:
            Resources, one per non-empty line of the response.
        """
        async with self.http_client.stream(  # type: ignore[attr-defined]
            "GET",
            self.build_path(),  # type: ignore[attr-defined]
            headers={"Accept": APPLICATION_JSONL},
        ) as response:
            async for line in response.aiter_lines():
                if line.strip():
                    yield self._model_class(json.loads(line))  # type: ignore[attr-defined]
