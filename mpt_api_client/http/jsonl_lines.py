import json
from collections.abc import AsyncIterable, AsyncIterator, Iterable, Iterator
from typing import Any


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

    Args:
        text_chunks: Decoded text chunks of the body, in arrival order.

    Yields:
        Each line without its line ending — a carriage return is stripped only as part
        of a CRLF ending, so a final unterminated line is yielded as-is; a blank line
        is yielded as an empty string, for the caller to skip.
    """
    pending = ""
    for chunk in text_chunks:
        lines = (pending + chunk).split("\n")
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

    Args:
        text_chunks: Decoded text chunks of the body, in arrival order.

    Yields:
        Each line without its line ending — a carriage return is stripped only as part
        of a CRLF ending, so a final unterminated line is yielded as-is; a blank line
        is yielded as an empty string, for the caller to skip.
    """
    pending = ""
    async for chunk in text_chunks:
        lines = (pending + chunk).split("\n")
        pending = lines.pop()
        for line in lines:
            yield line.removesuffix("\r")
    if pending:
        yield pending
