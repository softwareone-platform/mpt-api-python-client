import json
from collections.abc import AsyncIterator, Iterator, Mapping
from contextlib import AsyncExitStack, ExitStack

from mpt_api_client.constants import (
    APPLICATION_JSONL,
    MPT_STREAMING_ENABLED,
    MPT_STREAMING_HEADER,
)
from mpt_api_client.exceptions import (
    MPTHttpError,
    MPTStreamingNotEnabledError,
    raise_streaming_error,
)
from mpt_api_client.http.mixins.queryable_mixin import QueryableMixin
from mpt_api_client.http.types import HeaderTypes
from mpt_api_client.models import AsyncProgress, Progress
from mpt_api_client.models import Model as BaseModel


def streaming_request_headers() -> HeaderTypes:
    """Build the headers that opt a collection request into streaming mode.

    Returns:
        Headers requesting streaming mode with line-delimited output.
    """
    return {
        "Accept": APPLICATION_JSONL,
        MPT_STREAMING_HEADER: MPT_STREAMING_ENABLED,
    }


def streaming_pagination_params(limit: int | None, offset: int | None) -> dict[str, int]:
    """Build the pagination query parameters of a streaming request.

    Unset values are omitted rather than defaulted, because streaming mode reads an
    absent ``limit`` as the full snapshot. Supplied values are sent as given: the server
    owns pagination-input validation, so the client adds no guard of its own.

    Args:
        limit: Maximum number of records to export, or None to omit the parameter.
        offset: Offset to send with the request, or None to omit the parameter.

    Returns:
        Query parameters for the request, without the parameters left unset.
    """
    supplied_params = {"limit": limit, "offset": offset}
    return {
        param_name: param_value
        for param_name, param_value in supplied_params.items()
        if param_value is not None
    }


def confirm_streaming_mode(response_headers: Mapping[str, str], path: str) -> None:
    """Verify the API answered a streaming request in streaming mode.

    Args:
        response_headers: Headers of the streaming response.
        path: Requested path, used to build the error message.

    Raises:
        MPTStreamingNotEnabledError: If the response does not echo the streaming header.
    """
    echoed_value = response_headers.get(MPT_STREAMING_HEADER)
    if echoed_value is None or echoed_value.strip().lower() != MPT_STREAMING_ENABLED:
        raise MPTStreamingNotEnabledError(path, echoed_value)


class StreamingMixin[Model: BaseModel](QueryableMixin):
    """Mixin providing the platform streaming read mode for a collection endpoint.

    Streaming mode is opted into with the ``MPT-Streaming`` request header on the regular
    collection route, so the same filters, ordering and field selection apply. It is
    distinct from `StreamJSONLMixin`, which consumes endpoints that assign
    ``application/jsonl`` their own meaning outside streaming mode.
    """

    def stream(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        progress: Progress | None = None,
    ) -> Iterator[Model]:
        """Stream a result set in streaming mode, yielding one model per record.

        Unlike ``iterate()``, which pages through the collection and deserializes whole
        pages, this consumes a single line-delimited response without buffering the body.
        Membership is fixed when the stream opens, so records added afterwards are absent.

        Args:
            limit: Number of records to export, counted from the start of the stream
                order. Left unset by default, which exports the full snapshot, as does
                an explicit ``-1``. Under a bounded limit the server reports the capped
                count rather than the uncapped number of matches.
            offset: Offset to send with the request. Sent as given rather than checked
                locally, so the server decides whether it is a valid input.
            progress: Optional progress receiver. `item_processed` is called once per
                record before it is yielded and `completed` once when the response body
                is fully consumed. `set_total_items` is never called.

        Yields:
            Resources, one per non-empty line of the response.

        Raises:
            MPTStreamingNotEnabledError: If the API does not confirm streaming mode.
            MPTStreamingNotSupportedError: If the resource cannot stream (``501``).
            MPTStreamingNotAcceptableError: If the requested format is unsupported (``406``).
        """
        path = self.build_path(  # type: ignore[attr-defined]
            streaming_pagination_params(limit, offset),
        )
        # ExitStack scopes the error guard to the stream open: the negotiation failure is
        # raised by __enter__, and a plain `with` would force the record loop into the try.
        with ExitStack() as stack:
            try:
                response = stack.enter_context(
                    self.http_client.stream(  # type: ignore[attr-defined]
                        "GET",
                        path,
                        headers=streaming_request_headers(),
                    )
                )
            except MPTHttpError as http_error:
                raise_streaming_error(http_error, path)
            confirm_streaming_mode(response.headers, path)
            for line in response.iter_lines():
                if not line.strip():
                    continue
                model = self._model_class(json.loads(line))  # type: ignore[attr-defined]
                if progress:
                    progress.item_processed()
                yield model
        if progress:
            progress.completed()


class AsyncStreamingMixin[Model: BaseModel](QueryableMixin):
    """Async mixin providing the platform streaming read mode for a collection endpoint.

    Streaming mode is opted into with the ``MPT-Streaming`` request header on the regular
    collection route, so the same filters, ordering and field selection apply. It is
    distinct from `AsyncStreamJSONLMixin`, which consumes endpoints that assign
    ``application/jsonl`` their own meaning outside streaming mode.
    """

    async def stream(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        progress: AsyncProgress | None = None,
    ) -> AsyncIterator[Model]:
        """Stream a result set in streaming mode, yielding one model per record.

        Unlike ``iterate()``, which pages through the collection and deserializes whole
        pages, this consumes a single line-delimited response without buffering the body.
        Membership is fixed when the stream opens, so records added afterwards are absent.

        Args:
            limit: Number of records to export, counted from the start of the stream
                order. Left unset by default, which exports the full snapshot, as does
                an explicit ``-1``. Under a bounded limit the server reports the capped
                count rather than the uncapped number of matches.
            offset: Offset to send with the request. Sent as given rather than checked
                locally, so the server decides whether it is a valid input.
            progress: Optional progress receiver. `item_processed` is awaited once per
                record before it is yielded and `completed` once when the response body
                is fully consumed. `set_total_items` is never called.

        Yields:
            Resources, one per non-empty line of the response.

        Raises:
            MPTStreamingNotEnabledError: If the API does not confirm streaming mode.
            MPTStreamingNotSupportedError: If the resource cannot stream (``501``).
            MPTStreamingNotAcceptableError: If the requested format is unsupported (``406``).
        """
        path = self.build_path(  # type: ignore[attr-defined]
            streaming_pagination_params(limit, offset),
        )
        # AsyncExitStack scopes the error guard to the stream open: the negotiation failure
        # is raised by __aenter__, and a plain `async with` would force the record loop
        # into the try.
        async with AsyncExitStack() as stack:
            try:
                response = await stack.enter_async_context(
                    self.http_client.stream(  # type: ignore[attr-defined]
                        "GET",
                        path,
                        headers=streaming_request_headers(),
                    )
                )
            except MPTHttpError as http_error:
                raise_streaming_error(http_error, path)
            confirm_streaming_mode(response.headers, path)
            async for line in response.aiter_lines():
                if not line.strip():
                    continue
                model = self._model_class(json.loads(line))  # type: ignore[attr-defined]
                if progress:
                    await progress.item_processed()  # noqa: WPS476
                yield model
        if progress:
            await progress.completed()
