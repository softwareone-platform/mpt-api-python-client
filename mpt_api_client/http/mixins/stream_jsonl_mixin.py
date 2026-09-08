from collections.abc import AsyncIterator, Iterator

from mpt_api_client.constants import APPLICATION_JSONL
from mpt_api_client.http.jsonl_lines import (
    aiter_jsonl_lines,
    decode_record_line,
    iter_jsonl_lines,
)
from mpt_api_client.http.mixins.queryable_mixin import QueryableMixin
from mpt_api_client.models import AsyncProgress, Progress
from mpt_api_client.models import Model as BaseModel


class StreamJSONLMixin[Model: BaseModel](QueryableMixin):
    """Mixin providing JSONL (NDJSON) streaming of a collection line by line."""

    def stream_jsonl(self, *, progress: Progress | None = None) -> Iterator[Model]:
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

        Raises:
            JSONDecodeError: If a line is not valid JSON, or decodes to anything but
                an object.
        """
        with self.http_client.stream(  # type: ignore[attr-defined]
            "GET",
            self.build_path(),  # type: ignore[attr-defined]
            headers={"Accept": APPLICATION_JSONL},
        ) as response:
            for line in iter_jsonl_lines(response.iter_text()):
                if not line.strip():
                    continue
                model = self._model_class(decode_record_line(line))  # type: ignore[attr-defined]
                if progress:
                    progress.item_processed()
                yield model
        if progress:
            progress.completed()


class AsyncStreamJSONLMixin[Model: BaseModel](QueryableMixin):
    """Async mixin providing JSONL (NDJSON) streaming of a collection line by line."""

    async def stream_jsonl(self, *, progress: AsyncProgress | None = None) -> AsyncIterator[Model]:
        """Stream resources from a JSONL endpoint, yielding one model per line.

        Unlike ``iterate()``, which paginates and deserializes full pages, this
        consumes a ``application/jsonl`` response line by line without buffering the
        whole body in memory.

        A loop that can leave before the last line — a ``break``, a ``return``, an
        exception — has to close this generator to release the response, which
        `contextlib.aclosing` does at the end of its block::

            from contextlib import aclosing

            async with aclosing(service.stream_jsonl()) as records:
                async for record in records:
                    break

        Without that wrapper the abandoned generator stays suspended holding the open
        response, because Python finalizes an async generator through the event loop's
        async-generator hook rather than when its last reference goes. The sync twin
        needs no wrapper on CPython, where dropping the last reference closes the
        generator promptly.

        Args:
            progress: Optional progress receiver. `item_processed` is awaited once
                per line before the model is yielded and `completed` once when the
                response body is fully consumed. `set_total_items` is never called
                because JSONL responses carry no total.

        Yields:
            Resources, one per non-empty line of the response.

        Raises:
            JSONDecodeError: If a line is not valid JSON, or decodes to anything but
                an object.
        """
        async with self.http_client.stream(  # type: ignore[attr-defined]
            "GET",
            self.build_path(),  # type: ignore[attr-defined]
            headers={"Accept": APPLICATION_JSONL},
        ) as response:
            async for line in aiter_jsonl_lines(response.aiter_text()):
                if not line.strip():
                    continue
                model = self._model_class(decode_record_line(line))  # type: ignore[attr-defined]
                if progress:
                    await progress.item_processed()  # noqa: WPS476
                yield model
        if progress:
            await progress.completed()
