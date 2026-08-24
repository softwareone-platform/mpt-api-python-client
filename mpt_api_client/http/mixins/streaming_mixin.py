import json
from collections.abc import AsyncIterator, Iterator, Mapping
from contextlib import AsyncExitStack, ExitStack

from httpx import Response as HTTPXResponse

from mpt_api_client.constants import (
    APPLICATION_JSONL,
    MPT_ITEM_COUNT_HEADER,
    MPT_STREAMING_ENABLED,
    MPT_STREAMING_HEADER,
)
from mpt_api_client.exceptions import (
    MPTHttpError,
    MPTStreamingIncompleteError,
    MPTStreamingItemCountMissingError,
    MPTStreamingNotEnabledError,
    raise_streaming_error,
)
from mpt_api_client.http.mixins.queryable_mixin import QueryableMixin
from mpt_api_client.http.types import HeaderTypes
from mpt_api_client.models import AsyncProgress, DeletionStub, Progress, is_deletion_stub
from mpt_api_client.models import Model as BaseModel
from mpt_api_client.models.model import Resource


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


def declared_item_count(response_headers: Mapping[str, str], path: str) -> int:
    """Read the item count a streaming response declared.

    Args:
        response_headers: Headers of the streaming response.
        path: Requested path, used to build the error message.

    Returns:
        The number of records the stream declared it will emit.

    Raises:
        MPTStreamingItemCountMissingError: If the ``MPT-Item-Count`` response header
            is absent or is not a non-negative integer.
    """
    header_value = response_headers.get(MPT_ITEM_COUNT_HEADER)
    if header_value is None:
        raise MPTStreamingItemCountMissingError(path, header_value)
    try:
        expected_count = int(header_value)
    except ValueError as parse_error:
        raise MPTStreamingItemCountMissingError(path, header_value) from parse_error
    if expected_count < 0:
        raise MPTStreamingItemCountMissingError(path, header_value)
    return expected_count


def iter_verified_lines(response: HTTPXResponse, path: str) -> Iterator[str]:
    """Iterate the record lines of a streaming response, verifying completeness.

    The declared record count is read from the ``MPT-Item-Count`` header before the
    first line is yielded, and compared with the number of yielded lines when the body
    ends, because a truncated body that terminates gracefully carries no other failure
    signal. Blank keep-alive lines are skipped and not counted. A consumer that closes
    the iterator early skips the comparison: only a body consumed to the end is verified.

    Args:
        response: Open streaming response to consume.
        path: Requested path, used to build error messages.

    Yields:
        Non-blank body lines, one per record.

    Raises:
        MPTStreamingItemCountMissingError: If the declared item count is absent or is
            not a non-negative integer.
        MPTStreamingIncompleteError: If the fully consumed body emitted a number of
            records different from the declared item count.
    """
    expected_count = declared_item_count(response.headers, path)
    received_count = 0
    for line in response.iter_lines():
        if not line.strip():
            continue
        received_count += 1
        yield line
    if received_count != expected_count:
        raise MPTStreamingIncompleteError(path, expected_count, received_count)


async def aiter_verified_lines(response: HTTPXResponse, path: str) -> AsyncIterator[str]:
    """Iterate the record lines of an async streaming response, verifying completeness.

    The declared record count is read from the ``MPT-Item-Count`` header before the
    first line is yielded, and compared with the number of yielded lines when the body
    ends, because a truncated body that terminates gracefully carries no other failure
    signal. Blank keep-alive lines are skipped and not counted. A consumer that closes
    the iterator early skips the comparison: only a body consumed to the end is verified.

    Args:
        response: Open streaming response to consume.
        path: Requested path, used to build error messages.

    Yields:
        Non-blank body lines, one per record.

    Raises:
        MPTStreamingItemCountMissingError: If the declared item count is absent or is
            not a non-negative integer.
        MPTStreamingIncompleteError: If the fully consumed body emitted a number of
            records different from the declared item count.
    """
    expected_count = declared_item_count(response.headers, path)
    received_count = 0
    async for line in response.aiter_lines():
        if not line.strip():
            continue
        received_count += 1
        yield line
    if received_count != expected_count:
        raise MPTStreamingIncompleteError(path, expected_count, received_count)


def deserialize_stream_record[Model: BaseModel](
    record: Resource,
    model_class: type[Model],
) -> Model | DeletionStub:
    """Deserialize one streamed record into a model or a deletion stub.

    A record marked with ``$meta.deleted`` becomes a `DeletionStub` instead of a model,
    because the contract guarantees only its ``id``: as a model it would carry a full set
    of None fields, indistinguishable from a record whose values really are unset, and
    writing it back would overwrite the stored record with nulls. Every record still
    produces exactly one object, stubs included, so a stub counts towards the declared
    item count.

    Args:
        record: Deserialized record read from one line of the stream.
        model_class: Model class of the streamed resource.

    Returns:
        A model for a data record, or a `DeletionStub` for a deletion stub.

    Raises:
        TypeError: If a deletion stub carries no string ``id``.
    """
    if is_deletion_stub(record):
        return DeletionStub.from_record(record)
    return model_class(record)


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
    ) -> Iterator[Model | DeletionStub]:
        """Stream a result set in streaming mode, yielding one object per record.

        Unlike ``iterate()``, which pages through the collection and deserializes whole
        pages, this consumes a single line-delimited response without buffering the body.
        Membership is fixed when the stream opens, so records added afterwards are absent.
        A member hard-deleted after that snapshot arrives as a deletion stub and is yielded
        as a `DeletionStub` rather than a model, so it cannot be ingested as a record.
        Once the body is fully consumed, the record count is verified against the
        ``MPT-Item-Count`` response header, so a short export raises instead of ending as
        a silently partial result. Closing the iterator early skips that check.

        Args:
            limit: Number of records to export, counted from the start of the stream
                order. Left unset by default, which exports the full snapshot, as does
                an explicit ``-1``. Under a bounded limit the server reports the capped
                count rather than the uncapped number of matches.
            offset: Offset to send with the request. Sent as given rather than checked
                locally, so the server decides whether it is a valid input.
            progress: Optional progress receiver. `item_processed` is called once per
                yielded object, stubs included, before it is yielded, and `completed` once
                when the response body is fully consumed and verified complete.
                `set_total_items` is never called.

        Yields:
            Resources, one per non-empty line of the response, each either a model or a
            `DeletionStub` for a member deleted after the membership snapshot.

        Raises:
            MPTStreamingNotEnabledError: If the API does not confirm streaming mode.
            MPTStreamingNotSupportedError: If the resource cannot stream (``501``).
            MPTStreamingNotAcceptableError: If the requested format is unsupported (``406``).
            MPTStreamingOverCapError: If the export exceeds the configured cap (``413``).
            MPTStreamingItemCountMissingError: If the response declares no usable item count.
            MPTStreamingIncompleteError: If the fully consumed stream does not match the
                declared item count.
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
            for line in iter_verified_lines(response, path):
                result = deserialize_stream_record(
                    json.loads(line),
                    self._model_class,  # type: ignore[attr-defined]
                )
                if progress:
                    progress.item_processed()
                yield result
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
    ) -> AsyncIterator[Model | DeletionStub]:
        """Stream a result set in streaming mode, yielding one object per record.

        Unlike ``iterate()``, which pages through the collection and deserializes whole
        pages, this consumes a single line-delimited response without buffering the body.
        Membership is fixed when the stream opens, so records added afterwards are absent.
        A member hard-deleted after that snapshot arrives as a deletion stub and is yielded
        as a `DeletionStub` rather than a model, so it cannot be ingested as a record.
        Once the body is fully consumed, the record count is verified against the
        ``MPT-Item-Count`` response header, so a short export raises instead of ending as
        a silently partial result. Closing the iterator early skips that check.

        Args:
            limit: Number of records to export, counted from the start of the stream
                order. Left unset by default, which exports the full snapshot, as does
                an explicit ``-1``. Under a bounded limit the server reports the capped
                count rather than the uncapped number of matches.
            offset: Offset to send with the request. Sent as given rather than checked
                locally, so the server decides whether it is a valid input.
            progress: Optional progress receiver. `item_processed` is awaited once per
                yielded object, stubs included, before it is yielded, and `completed` once
                when the response body is fully consumed and verified complete.
                `set_total_items` is never called.

        Yields:
            Resources, one per non-empty line of the response, each either a model or a
            `DeletionStub` for a member deleted after the membership snapshot.

        Raises:
            MPTStreamingNotEnabledError: If the API does not confirm streaming mode.
            MPTStreamingNotSupportedError: If the resource cannot stream (``501``).
            MPTStreamingNotAcceptableError: If the requested format is unsupported (``406``).
            MPTStreamingOverCapError: If the export exceeds the configured cap (``413``).
            MPTStreamingItemCountMissingError: If the response declares no usable item count.
            MPTStreamingIncompleteError: If the fully consumed stream does not match the
                declared item count.
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
            async for line in aiter_verified_lines(response, path):
                result = deserialize_stream_record(
                    json.loads(line),
                    self._model_class,  # type: ignore[attr-defined]
                )
                if progress:
                    await progress.item_processed()  # noqa: WPS476
                yield result
        if progress:
            await progress.completed()
