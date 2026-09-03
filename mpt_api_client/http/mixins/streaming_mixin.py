from collections.abc import AsyncIterator, Iterator, Mapping
from contextlib import AsyncExitStack, ExitStack
from enum import StrEnum
from typing import Literal, overload

from httpx import Response as HTTPXResponse

from mpt_api_client.constants import (
    APPLICATION_JSON,
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
from mpt_api_client.http.json_envelope_parser import (
    JSONEnvelopeParser,
    StreamedRecord,
    StreamedTotal,
    StreamEvent,
)
from mpt_api_client.http.jsonl_lines import (
    aiter_jsonl_lines,
    decode_record_line,
    iter_jsonl_lines,
)
from mpt_api_client.http.mixins.queryable_mixin import QueryableMixin
from mpt_api_client.http.types import HeaderTypes
from mpt_api_client.models import AsyncProgress, DeletionStub, Progress, is_deletion_stub
from mpt_api_client.models import Model as BaseModel
from mpt_api_client.models.model import Resource


class StreamFormat(StrEnum):
    """Wire format a streaming read asks the API for with the ``Accept`` header.

    Both formats carry the same records and the same counts, so the choice is per
    request: `JSONL` is one record object per line with no envelope, `JSON` is the
    standard ``{$meta, data}`` list envelope the paged read path also returns.
    """

    JSONL = APPLICATION_JSONL
    JSON = APPLICATION_JSON


def streaming_request_headers(stream_format: StreamFormat) -> HeaderTypes:
    """Build the headers that opt a collection request into streaming mode.

    Args:
        stream_format: Wire format requested for the response body.

    Returns:
        Headers requesting streaming mode in the given format.
    """
    return {
        "Accept": stream_format.value,
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


def confirm_stream_format(
    response_headers: Mapping[str, str],
    path: str,
    stream_format: StreamFormat,
) -> None:
    """Verify the response is served in the requested wire format.

    A server or intermediary that echoes streaming mode but ignores ``Accept`` would
    hand the body to the parser of the other format — in the narrowest case a one-line
    envelope read as line-delimited records passes the count check and yields the whole
    envelope as one bogus record. Only a ``Content-Type`` naming a different media type
    rejects the response, before its body is consumed; a response without the header is
    tolerated.

    Args:
        response_headers: Headers of the streaming response.
        path: Requested path, used to build the error message.
        stream_format: Wire format the request asked for.

    Raises:
        MPTStreamingFormatMismatchError: If ``Content-Type`` names another media type.
    """
    content_type = response_headers.get(CONTENT_TYPE_HEADER)
    if content_type is None:
        return
    media_type = content_type.split(";")[0].strip().lower()
    if media_type != stream_format.value:
        raise MPTStreamingFormatMismatchError(path, stream_format.value, media_type)


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
    Lines are split on newlines alone, so a record carrying a Unicode line separator
    inside a string value stays whole.

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
    for line in iter_jsonl_lines(response.iter_text()):
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
    Lines are split on newlines alone, so a record carrying a Unicode line separator
    inside a string value stays whole.

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
    async for line in aiter_jsonl_lines(response.aiter_text()):
        if not line.strip():
            continue
        received_count += 1
        yield line
    if received_count != expected_count:
        raise MPTStreamingIncompleteError(path, expected_count, received_count)


def iter_jsonl_events(response: HTTPXResponse, path: str) -> Iterator[StreamEvent]:
    """Iterate the events of a line-delimited streaming response.

    Args:
        response: Open streaming response to consume.
        path: Requested path, used to build error messages.

    Yields:
        One record event per record line. The format carries no envelope, so it never
        reports a total.

    Raises:
        MPTStreamingItemCountMissingError: If the declared item count is absent or is
            not a non-negative integer.
        MPTStreamingIncompleteError: If the fully consumed body emitted a number of
            records different from the declared item count.
        JSONDecodeError: If a record line is not valid JSON, or decodes to anything
            but an object.
    """
    for line in iter_verified_lines(response, path):
        yield StreamedRecord(decode_record_line(line))


async def aiter_jsonl_events(response: HTTPXResponse, path: str) -> AsyncIterator[StreamEvent]:
    """Iterate the events of a line-delimited async streaming response.

    Args:
        response: Open streaming response to consume.
        path: Requested path, used to build error messages.

    Yields:
        One record event per record line. The format carries no envelope, so it never
        reports a total.

    Raises:
        MPTStreamingItemCountMissingError: If the declared item count is absent or is
            not a non-negative integer.
        MPTStreamingIncompleteError: If the fully consumed body emitted a number of
            records different from the declared item count.
        JSONDecodeError: If a record line is not valid JSON, or decodes to anything
            but an object.
    """
    async for line in aiter_verified_lines(response, path):
        yield StreamedRecord(decode_record_line(line))


def iter_envelope_events(
    response: HTTPXResponse,
    path: str,
    data_field: str,
) -> Iterator[StreamEvent]:
    """Iterate the events of a JSON envelope streaming response, verifying completeness.

    The body is tokenized as it arrives, so a record is emitted when its own closing
    brace arrives rather than when the envelope completes, and the whole body is never
    held in memory. Completeness is verified exactly as it is for the line-delimited
    format, against the ``MPT-Item-Count`` header.

    Args:
        response: Open streaming response to consume.
        path: Requested path, used to build error messages.
        data_field: Envelope member carrying the record array.

    Yields:
        One record event per record, and one event for the total the envelope reports.

    Raises:
        MPTStreamingItemCountMissingError: If the declared item count is absent or is
            not a non-negative integer.
        MPTStreamingIncompleteError: If the fully consumed body carried a number of
            records different from the declared item count.
        JSONDecodeError: If the body is not a well-formed envelope, or ends before
            closing it.
    """
    expected_count = declared_item_count(response.headers, path)
    parser = JSONEnvelopeParser(data_field)
    received_count = 0
    for chunk in response.iter_text():
        for event in parser.feed(chunk):
            if isinstance(event, StreamedRecord):
                received_count += 1
            yield event
    verify_envelope_end(parser, path, expected_count, received_count)


async def aiter_envelope_events(
    response: HTTPXResponse,
    path: str,
    data_field: str,
) -> AsyncIterator[StreamEvent]:
    """Iterate the events of an async JSON envelope response, verifying completeness.

    The body is tokenized as it arrives, so a record is emitted when its own closing
    brace arrives rather than when the envelope completes, and the whole body is never
    held in memory. Completeness is verified exactly as it is for the line-delimited
    format, against the ``MPT-Item-Count`` header.

    Args:
        response: Open streaming response to consume.
        path: Requested path, used to build error messages.
        data_field: Envelope member carrying the record array.

    Yields:
        One record event per record, and one event for the total the envelope reports.

    Raises:
        MPTStreamingItemCountMissingError: If the declared item count is absent or is
            not a non-negative integer.
        MPTStreamingIncompleteError: If the fully consumed body carried a number of
            records different from the declared item count.
        JSONDecodeError: If the body is not a well-formed envelope, or ends before
            closing it.
    """
    expected_count = declared_item_count(response.headers, path)
    parser = JSONEnvelopeParser(data_field)
    received_count = 0
    async for chunk in response.aiter_text():
        for event in parser.feed(chunk):
            if isinstance(event, StreamedRecord):
                received_count += 1
            yield event
    verify_envelope_end(parser, path, expected_count, received_count)


def verify_envelope_end(
    parser: JSONEnvelopeParser,
    path: str,
    expected_count: int,
    received_count: int,
) -> None:
    """Verify a consumed envelope carried every declared record and was closed.

    The record count is checked before the envelope structure, because a body cut short
    loses records before it loses its closing tokens, and a short export is the more
    precise diagnosis of the two.

    Args:
        parser: Parser fed the whole body.
        path: Requested path, used to build error messages.
        expected_count: Record count the response declared.
        received_count: Number of records the body actually carried.

    Raises:
        MPTStreamingIncompleteError: If the counts differ.
        JSONDecodeError: If the body ended before the envelope was closed.
    """
    if received_count != expected_count:
        raise MPTStreamingIncompleteError(path, expected_count, received_count)
    parser.close()


def iter_stream_events(
    response: HTTPXResponse,
    path: str,
    stream_format: StreamFormat,
    data_field: str,
) -> Iterator[StreamEvent]:
    """Iterate the events of a streaming response in the format it was requested in.

    Args:
        response: Open streaming response to consume.
        path: Requested path, used to build error messages.
        stream_format: Wire format the request asked for.
        data_field: Envelope member carrying the record array, in envelope format.

    Returns:
        Events of the response body, in arrival order.
    """
    if stream_format is StreamFormat.JSON:
        return iter_envelope_events(response, path, data_field)
    return iter_jsonl_events(response, path)


def aiter_stream_events(
    response: HTTPXResponse,
    path: str,
    stream_format: StreamFormat,
    data_field: str,
) -> AsyncIterator[StreamEvent]:
    """Iterate the events of an async streaming response in its requested format.

    Args:
        response: Open streaming response to consume.
        path: Requested path, used to build error messages.
        stream_format: Wire format the request asked for.
        data_field: Envelope member carrying the record array, in envelope format.

    Returns:
        Events of the response body, in arrival order.
    """
    if stream_format is StreamFormat.JSON:
        return aiter_envelope_events(response, path, data_field)
    return aiter_jsonl_events(response, path)


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
    def stream(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        stream_format: StreamFormat = StreamFormat.JSONL,
        progress: Progress | None = None,
        skip_deleted: Literal[True],
    ) -> Iterator[Model]: ...

    @overload
    def stream(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        stream_format: StreamFormat = StreamFormat.JSONL,
        progress: Progress | None = None,
        skip_deleted: Literal[False] = False,
    ) -> Iterator[Model | DeletionStub]: ...

    @overload
    def stream(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        stream_format: StreamFormat = StreamFormat.JSONL,
        progress: Progress | None = None,
        skip_deleted: bool,
    ) -> Iterator[Model | DeletionStub]: ...

    def stream(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        stream_format: StreamFormat = StreamFormat.JSONL,
        progress: Progress | None = None,
        skip_deleted: bool = False,
    ) -> Iterator[Model | DeletionStub]:
        """Stream a result set in streaming mode, yielding one object per record.

        Unlike ``iterate()``, which pages through the collection and deserializes whole
        pages, this consumes a single response as it arrives, without buffering the body:
        records are yielded while the rest of the export is still on the wire, in both
        wire formats. Membership is fixed when the stream opens, so records added
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
            stream_format: Wire format requested with ``Accept``. Defaults to the
                line-delimited format; `StreamFormat.JSON` reads the same records out of
                the standard ``{$meta, data}`` envelope instead, parsed incrementally.
                A member's ``Accept`` string is coerced to the member; any other value
                raises `ValueError` before the request is sent.
            progress: Optional progress receiver. `item_processed` is called once per
                record, stubs included — even a stub withheld by ``skip_deleted``, so a
                progress report still reaches the declared total — and `completed` once
                when the response body is fully consumed and verified complete.
                `set_total_items` is called exactly once, with the declared
                ``MPT-Item-Count``, as soon as the response headers are verified —
                before the first record, in both wire formats; the envelope's mirror
                of that count in ``$meta.pagination.total`` is not re-reported.
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
            MPTStreamingNotEnabledError: If the API does not confirm streaming mode.
            MPTStreamingFormatMismatchError: If the response ``Content-Type`` names a
                media type other than the requested format.
            MPTStreamingNotSupportedError: If the resource cannot stream (``501``).
            MPTStreamingNotAcceptableError: If the requested format is unsupported (``406``).
            MPTStreamingOverCapError: If the export exceeds the configured cap (``413``).
            MPTStreamingItemCountMissingError: If the response declares no usable item count.
            MPTStreamingIncompleteError: If the fully consumed stream does not match the
                declared item count.
            JSONDecodeError: If the body cannot be parsed in the requested wire format —
                a malformed or non-object record line in the line-delimited format, or a
                malformed or unterminated envelope in the envelope format.
            ValueError: If ``stream_format`` is neither a `StreamFormat` member nor a
                member's value.
        """
        # Coerce eagerly: an equal plain string becomes its member, anything else fails
        # with a clear ValueError instead of an AttributeError deep in header building.
        stream_format = StreamFormat(stream_format)
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
                        headers=streaming_request_headers(stream_format),
                    )
                )
            except MPTHttpError as http_error:
                raise_streaming_error(http_error, path)
            confirm_streaming_mode(response.headers, path)
            confirm_stream_format(response.headers, path, stream_format)
            if progress:
                progress.set_total_items(declared_item_count(response.headers, path))
            events = iter_stream_events(
                response,
                path,
                stream_format,
                self._collection_key,  # type: ignore[attr-defined]
            )
            yield from self._stream_results(events, progress, skip_deleted=skip_deleted)
        if progress:
            progress.completed()

    def _stream_results(
        self,
        events: Iterator[StreamEvent],
        progress: Progress | None,
        *,
        skip_deleted: bool,
    ) -> Iterator[Model | DeletionStub]:
        # A withheld stub was still ticked upstream: the declared total includes stubs,
        # so a progress report fed only visible records would never reach it.
        for result in self._deserialized_results(events, progress):
            if skip_deleted and isinstance(result, DeletionStub):
                continue
            yield result

    def _deserialized_results(
        self,
        events: Iterator[StreamEvent],
        progress: Progress | None,
    ) -> Iterator[Model | DeletionStub]:
        for event in events:
            if isinstance(event, StreamedTotal):
                # The envelope total mirrors MPT-Item-Count (TDR 4.6), which already
                # fed the receiver; forwarding the copy could only overwrite the
                # authoritative value when a faulty response makes them differ.
                continue
            result = deserialize_stream_record(
                event.record,
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
    def stream(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        stream_format: StreamFormat = StreamFormat.JSONL,
        progress: AsyncProgress | None = None,
        skip_deleted: Literal[True],
    ) -> AsyncIterator[Model]: ...

    @overload
    def stream(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        stream_format: StreamFormat = StreamFormat.JSONL,
        progress: AsyncProgress | None = None,
        skip_deleted: Literal[False] = False,
    ) -> AsyncIterator[Model | DeletionStub]: ...

    @overload
    def stream(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        stream_format: StreamFormat = StreamFormat.JSONL,
        progress: AsyncProgress | None = None,
        skip_deleted: bool,
    ) -> AsyncIterator[Model | DeletionStub]: ...

    async def stream(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        stream_format: StreamFormat = StreamFormat.JSONL,
        progress: AsyncProgress | None = None,
        skip_deleted: bool = False,
    ) -> AsyncIterator[Model | DeletionStub]:
        """Stream a result set in streaming mode, yielding one object per record.

        Unlike ``iterate()``, which pages through the collection and deserializes whole
        pages, this consumes a single response as it arrives, without buffering the body:
        records are yielded while the rest of the export is still on the wire, in both
        wire formats. Membership is fixed when the stream opens, so records added
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
            stream_format: Wire format requested with ``Accept``. Defaults to the
                line-delimited format; `StreamFormat.JSON` reads the same records out of
                the standard ``{$meta, data}`` envelope instead, parsed incrementally.
                A member's ``Accept`` string is coerced to the member; any other value
                raises `ValueError` before the request is sent.
            progress: Optional progress receiver. `item_processed` is awaited once per
                record, stubs included — even a stub withheld by ``skip_deleted``, so a
                progress report still reaches the declared total — and `completed` once
                when the response body is fully consumed and verified complete.
                `set_total_items` is called exactly once, with the declared
                ``MPT-Item-Count``, as soon as the response headers are verified —
                before the first record, in both wire formats; the envelope's mirror
                of that count in ``$meta.pagination.total`` is not re-reported.
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
            MPTStreamingNotEnabledError: If the API does not confirm streaming mode.
            MPTStreamingFormatMismatchError: If the response ``Content-Type`` names a
                media type other than the requested format.
            MPTStreamingNotSupportedError: If the resource cannot stream (``501``).
            MPTStreamingNotAcceptableError: If the requested format is unsupported (``406``).
            MPTStreamingOverCapError: If the export exceeds the configured cap (``413``).
            MPTStreamingItemCountMissingError: If the response declares no usable item count.
            MPTStreamingIncompleteError: If the fully consumed stream does not match the
                declared item count.
            JSONDecodeError: If the body cannot be parsed in the requested wire format —
                a malformed or non-object record line in the line-delimited format, or a
                malformed or unterminated envelope in the envelope format.
            ValueError: If ``stream_format`` is neither a `StreamFormat` member nor a
                member's value.
        """
        # Coerce eagerly: an equal plain string becomes its member, anything else fails
        # with a clear ValueError instead of an AttributeError deep in header building.
        stream_format = StreamFormat(stream_format)
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
                        headers=streaming_request_headers(stream_format),
                    )
                )
            except MPTHttpError as http_error:
                raise_streaming_error(http_error, path)
            confirm_streaming_mode(response.headers, path)
            confirm_stream_format(response.headers, path, stream_format)
            if progress:
                await progress.set_total_items(declared_item_count(response.headers, path))
            async for result in self._stream_results(
                aiter_stream_events(
                    response,
                    path,
                    stream_format,
                    self._collection_key,  # type: ignore[attr-defined]
                ),
                progress,
                skip_deleted=skip_deleted,
            ):
                yield result
        if progress:
            await progress.completed()

    async def _stream_results(
        self,
        events: AsyncIterator[StreamEvent],
        progress: AsyncProgress | None,
        *,
        skip_deleted: bool,
    ) -> AsyncIterator[Model | DeletionStub]:
        # A withheld stub was still ticked upstream: the declared total includes stubs,
        # so a progress report fed only visible records would never reach it.
        async for result in self._deserialized_results(events, progress):
            if skip_deleted and isinstance(result, DeletionStub):
                continue
            yield result

    async def _deserialized_results(
        self,
        events: AsyncIterator[StreamEvent],
        progress: AsyncProgress | None,
    ) -> AsyncIterator[Model | DeletionStub]:
        async for event in events:
            if isinstance(event, StreamedTotal):
                # The envelope total mirrors MPT-Item-Count (TDR 4.6), which already
                # fed the receiver; forwarding the copy could only overwrite the
                # authoritative value when a faulty response makes them differ.
                continue
            result = deserialize_stream_record(
                event.record,
                self._model_class,  # type: ignore[attr-defined]
            )
            if progress:
                await progress.item_processed()  # noqa: WPS476
            yield result
