import json
from collections.abc import AsyncIterable, AsyncIterator, Iterable, Iterator
from typing import Any

from mpt_api_client.constants import UTF8_BOM


def decode_record_line(line: str) -> dict[str, Any]:
    """Decode one record line of a JSONL body.

    The decoded value is required to be an object, the same guard the envelope parser
    applies to its record elements: a valid-JSON line holding anything else fails here
    as the documented decode error instead of an arbitrary error — or a silently empty
    record — out of whatever consumes the value next.

    Args:
        line: Non-blank body line carrying one record.

    Returns:
        The decoded record.

    Raises:
        JSONDecodeError: If the line is not valid JSON, or decodes to anything but
            an object.
    """
    record = json.loads(line)
    if not isinstance(record, dict):
        raise json.JSONDecodeError("JSONL record must be an object", line, 0)
    return record


def iter_jsonl_lines(text_chunks: Iterable[str]) -> Iterator[str]:
    """Iterate the lines of a JSONL body, splitting on newlines alone.

    A JSONL record ends at a line feed, optionally preceded by a carriage return.
    Splitting with ``str.splitlines()`` semantics — what ``httpx``'s ``iter_lines()``
    does — would also break at U+2028, U+2029 and U+0085, which are legal unescaped
    inside a JSON string value, fracturing such a record into unparseable fragments.
    A single byte order mark opening the body is dropped before the first line is
    formed, and only there: the sibling read paths tolerate exactly that one — the
    paged path's ``json.loads`` on raw bytes strips it, and the envelope parser skips
    it at envelope start — so a BOM-emitting producer parses the same in every format.

    Args:
        text_chunks: Decoded text chunks of the body, in arrival order.

    Yields:
        Each line without its line ending — a carriage return is stripped only as part
        of a CRLF ending, so a final unterminated line is yielded as-is; a blank line
        is yielded as an empty string, for the caller to skip.
    """
    pending = ""
    at_body_start = True
    for chunk in text_chunks:
        if at_body_start and chunk:
            # `pending` is necessarily empty before the first non-empty chunk, so the
            # body's first character — the only place a BOM is tolerated — is its start.
            pending = chunk.removeprefix(UTF8_BOM)
            at_body_start = False
        else:
            pending += chunk
        lines = pending.split("\n")
        pending = lines.pop()
        for line in lines:
            yield line.removesuffix("\r")
    if pending:
        yield pending


async def aiter_jsonl_lines(text_chunks: AsyncIterable[str]) -> AsyncIterator[str]:
    """Iterate the lines of an async JSONL body, splitting on newlines alone.

    A JSONL record ends at a line feed, optionally preceded by a carriage return.
    Splitting with ``str.splitlines()`` semantics — what ``httpx``'s ``aiter_lines()``
    does — would also break at U+2028, U+2029 and U+0085, which are legal unescaped
    inside a JSON string value, fracturing such a record into unparseable fragments.
    A single byte order mark opening the body is dropped before the first line is
    formed, and only there: the sibling read paths tolerate exactly that one — the
    paged path's ``json.loads`` on raw bytes strips it, and the envelope parser skips
    it at envelope start — so a BOM-emitting producer parses the same in every format.

    Args:
        text_chunks: Decoded text chunks of the body, in arrival order.

    Yields:
        Each line without its line ending — a carriage return is stripped only as part
        of a CRLF ending, so a final unterminated line is yielded as-is; a blank line
        is yielded as an empty string, for the caller to skip.
    """
    pending = ""
    at_body_start = True
    async for chunk in text_chunks:
        if at_body_start and chunk:
            # `pending` is necessarily empty before the first non-empty chunk, so the
            # body's first character — the only place a BOM is tolerated — is its start.
            pending = chunk.removeprefix(UTF8_BOM)
            at_body_start = False
        else:
            pending += chunk
        lines = pending.split("\n")
        pending = lines.pop()
        for line in lines:
            yield line.removesuffix("\r")
    if pending:
        yield pending
