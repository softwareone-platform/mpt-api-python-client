import re
from collections.abc import AsyncIterator, Iterator, Mapping
from contextlib import AsyncExitStack, ExitStack
from enum import StrEnum
from typing import Literal, overload

from httpx import Response as HTTPXResponse

from mpt_api_client.constants import (
    APPLICATION_JSONL,
    CONTENT_TYPE_HEADER,
    MPT_ITEM_COUNT_HEADER,
    MPT_STREAMING_ENABLED,
    MPT_STREAMING_HEADER,
)
from mpt_api_client.exceptions import (
    MPTHttpError,
    MPTStreamingFormatMismatchError,
    MPTStreamingIncompleteError,
    MPTStreamingItemCountMissingError,
    MPTStreamingNotEnabledError,
    raise_streaming_error,
)
from mpt_api_client.http.jsonl_lines import (
    aiter_jsonl_lines,
    decode_record_line,
    is_keep_alive_line,
    iter_jsonl_lines,
)
from mpt_api_client.http.mixins.queryable_mixin import QueryableMixin
from mpt_api_client.http.types import HeaderTypes
from mpt_api_client.models import AsyncProgress, DeletionStub, Progress, is_deletion_stub
from mpt_api_client.models import Model as BaseModel
from mpt_api_client.models.model import Resource

# The canonical count form: ASCII digits only. ``re.ASCII`` is load-bearing: a bare ``\d``
# is Unicode-aware and would match U+0665 and its kin, re-admitting the non-ASCII digits
# this guard exists to reject. A bare int() would also admit Python literal forms — '1_0',
# '+5', ' 5 ' — silently normalizing a garbled header into a wrong count instead of
# rejecting it before the body is consumed.
ITEM_COUNT_PATTERN = re.compile(r"\d+", re.ASCII)


class StreamFormat(StrEnum):
    """Wire format a streaming read asks the API for with the ``Accept`` header.

    Only the line-delimited format is served: one record object per line, no envelope.
    The enum is a single member rather than a bare constant so that re-adding the
    ``{$meta, data}`` envelope later costs no change to any public name.
    """

    JSONL = APPLICATION_JSONL


def streaming_request_headers() -> HeaderTypes:
    """Build the headers that opt a collection request into streaming mode.

    Returns:
        Headers requesting streaming mode in the line-delimited format.
    """
    return {
        "Accept": StreamFormat.JSONL.value,
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


def confirm_stream_format(response_headers: Mapping[str, str], path: str) -> None:
    """Verify the response is served in the line-delimited format the request asked for.

    A server or intermediary that echoes streaming mode but ignores ``Accept`` would hand
    the body to the wrong reader — in the narrowest case a one-line ``{$meta, data}``
    envelope read as line-delimited records passes the count check and yields the whole
    envelope as one bogus record. Only a ``Content-Type`` naming a different media type
    rejects the response, before its body is consumed; a response without the header is
    tolerated.

    Args:
        response_headers: Headers of the streaming response.
        path: Requested path, used to build the error message.

    Raises:
        MPTStreamingFormatMismatchError: If ``Content-Type`` names another media type.
    """
    content_type = response_headers.get(CONTENT_TYPE_HEADER)
    if content_type is None:
        return
    expected = StreamFormat.JSONL.value
    media_type = content_type.split(";")[0].strip().lower()
    if media_type != expected:
        raise MPTStreamingFormatMismatchError(path, expected, media_type)


def declared_item_count(response_headers: Mapping[str, str], path: str) -> int:
    """Read the item count a streaming response declared.

    Args:
        response_headers: Headers of the streaming response.
        path: Requested path, used to build the error message.

    Returns:
        The number of records the stream declared it will emit.

    Raises:
        MPTStreamingItemCountMissingError: If the ``MPT-Item-Count`` response header
            is absent or is not a canonical non-negative integer: ASCII digits only.
    """
    header_value = response_headers.get(MPT_ITEM_COUNT_HEADER)
    if header_value is None or not ITEM_COUNT_PATTERN.fullmatch(header_value):
        raise MPTStreamingItemCountMissingError(path, header_value)
    return int(header_value)


def iter_verified_lines(response: HTTPXResponse, path: str) -> Iterator[str]:
    """Iterate the record lines of a streaming response, verifying completeness.

    The declared record count is read from the ``MPT-Item-Count`` header before the
    first line is yielded, and compared with the number of yielded lines when the body
    ends, because a truncated body that terminates gracefully carries no other failure
    signal. Keep-alive lines are skipped and not counted, and only JSON's own insignificant
    whitespace makes a line one: a line of U+00A0, U+2028 or U+001E is a malformed record,
    counted and decoded rather than waved through. A consumer that closes the iterator early
    skips the comparison: only a body consumed to the end is verified. Lines are split on
    newlines alone, so a record carrying a Unicode line separator inside a string value
    stays whole.

    Args:
        response: Open streaming response to consume.
        path: Requested path, used to build error messages.

    Yields:
        Body lines other than keep-alives, one per record.

    Raises:
        MPTStreamingItemCountMissingError: If the declared item count is absent or is
            not a canonical non-negative integer.
        MPTStreamingIncompleteError: If the fully consumed body emitted a number of
            records different from the declared item count.
    """
    expected_count = declared_item_count(response.headers, path)
    received_count = 0
    for line in iter_jsonl_lines(response.iter_text()):
        if is_keep_alive_line(line):
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
    signal. Keep-alive lines are skipped and not counted, and only JSON's own insignificant
    whitespace makes a line one: a line of U+00A0, U+2028 or U+001E is a malformed record,
    counted and decoded rather than waved through. A consumer that closes the iterator early
    skips the comparison: only a body consumed to the end is verified. Lines are split on
    newlines alone, so a record carrying a Unicode line separator inside a string value
    stays whole.

    Args:
        response: Open streaming response to consume.
        path: Requested path, used to build error messages.

    Yields:
        Body lines other than keep-alives, one per record.

    Raises:
        MPTStreamingItemCountMissingError: If the declared item count is absent or is
            not a canonical non-negative integer.
        MPTStreamingIncompleteError: If the fully consumed body emitted a number of
            records different from the declared item count.
    """
    expected_count = declared_item_count(response.headers, path)
    received_count = 0
    async for line in aiter_jsonl_lines(response.aiter_text()):
        if is_keep_alive_line(line):
            continue
        received_count += 1
        yield line
    if received_count != expected_count:
        raise MPTStreamingIncompleteError(path, expected_count, received_count)


def iter_jsonl_records(response: HTTPXResponse, path: str) -> Iterator[Resource]:
    """Iterate the records of a line-delimited streaming response.

    Args:
        response: Open streaming response to consume.
        path: Requested path, used to build error messages.

    Yields:
        One decoded record per record line.

    Raises:
        MPTStreamingItemCountMissingError: If the declared item count is absent or is
            not a canonical non-negative integer.
        MPTStreamingIncompleteError: If the fully consumed body emitted a number of
            records different from the declared item count.
        JSONDecodeError: If a record line is not valid JSON, or decodes to anything
            but an object.
    """
    for line in iter_verified_lines(response, path):
        yield decode_record_line(line)


async def aiter_jsonl_records(response: HTTPXResponse, path: str) -> AsyncIterator[Resource]:
    """Iterate the records of a line-delimited async streaming response.

    Args:
        response: Open streaming response to consume.
        path: Requested path, used to build error messages.

    Yields:
        One decoded record per record line.

    Raises:
        MPTStreamingItemCountMissingError: If the declared item count is absent or is
            not a canonical non-negative integer.
        MPTStreamingIncompleteError: If the fully consumed body emitted a number of
            records different from the declared item count.
        JSONDecodeError: If a record line is not valid JSON, or decodes to anything
            but an object.
    """
    async for line in aiter_verified_lines(response, path):
        yield decode_record_line(line)


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

    @overload
    def stream_snapshot(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        progress: Progress | None = None,
        skip_deleted: Literal[True],
    ) -> Iterator[Model]: ...

    @overload
    def stream_snapshot(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        progress: Progress | None = None,
        skip_deleted: Literal[False] = False,
    ) -> Iterator[Model | DeletionStub]: ...

    @overload
    def stream_snapshot(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        progress: Progress | None = None,
        skip_deleted: bool,
    ) -> Iterator[Model | DeletionStub]: ...

    def stream_snapshot(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        progress: Progress | None = None,
        skip_deleted: bool = False,
    ) -> Iterator[Model | DeletionStub]:
        """Stream a result set in streaming mode, yielding one object per record.

        Unlike ``iterate()``, which pages through the collection and deserializes whole
        pages, this consumes a single response as it arrives, without buffering the body:
        records are yielded while the rest of the export is still on the wire.
        Membership is fixed when the stream opens, so records added
        afterwards are absent.
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
                record, stubs included — even a stub withheld by ``skip_deleted``, so a
                progress report still reaches the declared total — and `completed` once
                when the response body is fully consumed and verified complete.
                `set_total_items` is called exactly once, with the declared
                ``MPT-Item-Count``, as soon as the response headers are verified,
                before the first record.
            skip_deleted: When set, deletion stubs are filtered out at yield time, for a
                consumer that does not ingest deletions and would otherwise write the
                ``isinstance`` branch only to drop the stubs. The completeness accounting
                counts raw records ahead of the filter, and the count is compared with
                ``MPT-Item-Count`` only once the body is fully consumed, so a short
                stream raises exactly as it does without the flag — records yielded
                before a truncated tail have been processed by then. The number of
                yielded objects intentionally falls short of ``MPT-Item-Count`` when the
                snapshot contains stubs. The default keeps the contract-faithful shape:
                one object per snapshot member, stubs visible.

        Yields:
            Resources, one per record of the response, each either a model or a
            `DeletionStub` for a member deleted after the membership snapshot; only the
            models when ``skip_deleted`` is set.

        Raises:
            MPTMaxRetryError: If opening the response fails after maximum retry attempts;
                transparent retry ends once the response commits, so it never follows
                the first record.
            MPTStreamingNotEnabledError: If the API does not confirm streaming mode.
            MPTStreamingFormatMismatchError: If the response ``Content-Type`` names a
                media type other than the line-delimited format.
            MPTStreamingNotSupportedError: If the resource cannot stream (``501``).
            MPTStreamingNotAcceptableError: If the format is unsupported (``406``).
            MPTStreamingOverCapError: If the export exceeds the configured cap (``413``).
            MPTStreamingItemCountMissingError: If the response declares no usable item count.
            MPTStreamingTruncatedError: If the connection aborts mid-body, ending the
                response before the HTTP message completes; the records yielded before
                the abort are an incomplete snapshot to discard.
            MPTStreamingIncompleteError: If the fully consumed stream does not match the
                declared item count.
            JSONDecodeError: If a record line is not valid JSON, or decodes to
                anything but an object.
            TypeError: If a deletion stub carries no string ``id``, the one property the
                contract guarantees on a stub.
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
            confirm_stream_format(response.headers, path)
            if progress:
                progress.set_total_items(declared_item_count(response.headers, path))
            records = iter_jsonl_records(response, path)
            yield from self._stream_results(records, progress, skip_deleted=skip_deleted)
        if progress:
            progress.completed()

    def _stream_results(
        self,
        records: Iterator[Resource],
        progress: Progress | None,
        *,
        skip_deleted: bool,
    ) -> Iterator[Model | DeletionStub]:
        # A withheld stub was still ticked upstream: the declared total includes stubs,
        # so a progress report fed only visible records would never reach it.
        for result in self._deserialized_results(records, progress):
            if skip_deleted and isinstance(result, DeletionStub):
                continue
            yield result

    def _deserialized_results(
        self,
        records: Iterator[Resource],
        progress: Progress | None,
    ) -> Iterator[Model | DeletionStub]:
        for record in records:
            result = deserialize_stream_record(
                record,
                self._model_class,  # type: ignore[attr-defined]
            )
            if progress:
                progress.item_processed()
            yield result


class AsyncStreamingMixin[Model: BaseModel](QueryableMixin):
    """Async mixin providing the platform streaming read mode for a collection endpoint.

    Streaming mode is opted into with the ``MPT-Streaming`` request header on the regular
    collection route, so the same filters, ordering and field selection apply. It is
    distinct from `AsyncStreamJSONLMixin`, which consumes endpoints that assign
    ``application/jsonl`` their own meaning outside streaming mode.
    """

    @overload
    def stream_snapshot(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        progress: AsyncProgress | None = None,
        skip_deleted: Literal[True],
    ) -> AsyncIterator[Model]: ...

    @overload
    def stream_snapshot(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        progress: AsyncProgress | None = None,
        skip_deleted: Literal[False] = False,
    ) -> AsyncIterator[Model | DeletionStub]: ...

    @overload
    def stream_snapshot(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        progress: AsyncProgress | None = None,
        skip_deleted: bool,
    ) -> AsyncIterator[Model | DeletionStub]: ...

    async def stream_snapshot(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        progress: AsyncProgress | None = None,
        skip_deleted: bool = False,
    ) -> AsyncIterator[Model | DeletionStub]:
        """Stream a result set in streaming mode, yielding one object per record.

        Unlike ``iterate()``, which pages through the collection and deserializes whole
        pages, this consumes a single response as it arrives, without buffering the body:
        records are yielded while the rest of the export is still on the wire.
        Membership is fixed when the stream opens, so records added
        afterwards are absent.
        A member hard-deleted after that snapshot arrives as a deletion stub and is yielded
        as a `DeletionStub` rather than a model, so it cannot be ingested as a record.
        Once the body is fully consumed, the record count is verified against the
        ``MPT-Item-Count`` response header, so a short export raises instead of ending as
        a silently partial result. Closing the iterator early skips that check.

        A loop that can leave before the last record — a ``break``, a ``return``, an
        exception — has to close this generator to release the response, which
        `contextlib.aclosing` does at the end of its block::

            from contextlib import aclosing

            async with aclosing(service.stream_snapshot()) as records:
                async for record in records:
                    break

        Without that wrapper the abandoned generator stays suspended holding the open
        response: Python finalizes an async generator through the event loop's
        async-generator hook rather than when its last reference goes, so the connection
        stays checked out of the pool until the hook runs. A long-lived service that
        breaks out of many streams accumulates connections that way and reports the debt
        as unclosed responses at loop shutdown. The sync twin needs no wrapper on CPython,
        where dropping the last reference closes the generator promptly.

        Args:
            limit: Number of records to export, counted from the start of the stream
                order. Left unset by default, which exports the full snapshot, as does
                an explicit ``-1``. Under a bounded limit the server reports the capped
                count rather than the uncapped number of matches.
            offset: Offset to send with the request. Sent as given rather than checked
                locally, so the server decides whether it is a valid input.
            progress: Optional progress receiver. `item_processed` is awaited once per
                record, stubs included — even a stub withheld by ``skip_deleted``, so a
                progress report still reaches the declared total — and `completed` once
                when the response body is fully consumed and verified complete.
                `set_total_items` is called exactly once, with the declared
                ``MPT-Item-Count``, as soon as the response headers are verified,
                before the first record.
            skip_deleted: When set, deletion stubs are filtered out at yield time, for a
                consumer that does not ingest deletions and would otherwise write the
                ``isinstance`` branch only to drop the stubs. The completeness accounting
                counts raw records ahead of the filter, and the count is compared with
                ``MPT-Item-Count`` only once the body is fully consumed, so a short
                stream raises exactly as it does without the flag — records yielded
                before a truncated tail have been processed by then. The number of
                yielded objects intentionally falls short of ``MPT-Item-Count`` when the
                snapshot contains stubs. The default keeps the contract-faithful shape:
                one object per snapshot member, stubs visible.

        Yields:
            Resources, one per record of the response, each either a model or a
            `DeletionStub` for a member deleted after the membership snapshot; only the
            models when ``skip_deleted`` is set.

        Raises:
            MPTMaxRetryError: If opening the response fails after maximum retry attempts;
                transparent retry ends once the response commits, so it never follows
                the first record.
            MPTStreamingNotEnabledError: If the API does not confirm streaming mode.
            MPTStreamingFormatMismatchError: If the response ``Content-Type`` names a
                media type other than the line-delimited format.
            MPTStreamingNotSupportedError: If the resource cannot stream (``501``).
            MPTStreamingNotAcceptableError: If the format is unsupported (``406``).
            MPTStreamingOverCapError: If the export exceeds the configured cap (``413``).
            MPTStreamingItemCountMissingError: If the response declares no usable item count.
            MPTStreamingTruncatedError: If the connection aborts mid-body, ending the
                response before the HTTP message completes; the records yielded before
                the abort are an incomplete snapshot to discard.
            MPTStreamingIncompleteError: If the fully consumed stream does not match the
                declared item count.
            JSONDecodeError: If a record line is not valid JSON, or decodes to
                anything but an object.
            TypeError: If a deletion stub carries no string ``id``, the one property the
                contract guarantees on a stub.
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
            confirm_stream_format(response.headers, path)
            if progress:
                await progress.set_total_items(declared_item_count(response.headers, path))
            async for result in self._stream_results(
                aiter_jsonl_records(response, path),
                progress,
                skip_deleted=skip_deleted,
            ):
                yield result
        if progress:
            await progress.completed()

    async def _stream_results(
        self,
        records: AsyncIterator[Resource],
        progress: AsyncProgress | None,
        *,
        skip_deleted: bool,
    ) -> AsyncIterator[Model | DeletionStub]:
        # A withheld stub was still ticked upstream: the declared total includes stubs,
        # so a progress report fed only visible records would never reach it.
        async for result in self._deserialized_results(records, progress):
            if skip_deleted and isinstance(result, DeletionStub):
                continue
            yield result

    async def _deserialized_results(
        self,
        records: AsyncIterator[Resource],
        progress: AsyncProgress | None,
    ) -> AsyncIterator[Model | DeletionStub]:
        async for record in records:
            result = deserialize_stream_record(
                record,
                self._model_class,  # type: ignore[attr-defined]
            )
            if progress:
                await progress.item_processed()  # noqa: WPS476
            yield result
