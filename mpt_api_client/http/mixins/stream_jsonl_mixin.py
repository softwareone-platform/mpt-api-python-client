import json
from collections.abc import AsyncIterator, Iterator

from mpt_api_client.constants import APPLICATION_JSONL
from mpt_api_client.http.mixins.queryable_mixin import QueryableMixin
from mpt_api_client.models import AsyncProgress, Progress
from mpt_api_client.models import Model as BaseModel


class StreamJSONLMixin[Model: BaseModel](QueryableMixin):
    """Mixin providing JSONL (NDJSON) streaming of a collection line by line."""

    def stream(self, *, progress: Progress | None = None) -> Iterator[Model]:
        """Stream resources from a JSONL endpoint, yielding one model per line.

        Unlike ``iterate()``, which paginates and deserializes full pages, this
        consumes a ``application/jsonl`` response line by line without buffering the
        whole body in memory.

        Args:
            progress: Optional progress receiver. `item_processed` is called once
                per line before the model is yielded and `completed` once when the
                response body is fully consumed. `set_total_items` is never called
                because JSONL responses carry no total.

        Yields:
            Resources, one per non-empty line of the response.
        """
        with self.http_client.stream(  # type: ignore[attr-defined]
            "GET",
            self.build_path(),  # type: ignore[attr-defined]
            headers={"Accept": APPLICATION_JSONL},
        ) as response:
            for line in response.iter_lines():
                if not line.strip():
                    continue
                model = self._model_class(json.loads(line))  # type: ignore[attr-defined]
                if progress:
                    progress.item_processed()
                yield model
        if progress:
            progress.completed()


class AsyncStreamJSONLMixin[Model: BaseModel](QueryableMixin):
    """Async mixin providing JSONL (NDJSON) streaming of a collection line by line."""

    async def stream(self, *, progress: AsyncProgress | None = None) -> AsyncIterator[Model]:
        """Stream resources from a JSONL endpoint, yielding one model per line.

        Unlike ``iterate()``, which paginates and deserializes full pages, this
        consumes a ``application/jsonl`` response line by line without buffering the
        whole body in memory.

        Args:
            progress: Optional progress receiver. `item_processed` is awaited once
                per line before the model is yielded and `completed` once when the
                response body is fully consumed. `set_total_items` is never called
                because JSONL responses carry no total.

        Yields:
            Resources, one per non-empty line of the response.
        """
        async with self.http_client.stream(  # type: ignore[attr-defined]
            "GET",
            self.build_path(),  # type: ignore[attr-defined]
            headers={"Accept": APPLICATION_JSONL},
        ) as response:
            async for line in response.aiter_lines():
                if not line.strip():
                    continue
                model = self._model_class(json.loads(line))  # type: ignore[attr-defined]
                if progress:
                    await progress.item_processed()  # noqa: WPS476
                yield model
        if progress:
            await progress.completed()
