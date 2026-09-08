import json
import re
from collections.abc import AsyncIterable, AsyncIterator, Iterable, Iterator
from typing import Any

from mpt_api_client.constants import UTF8_BOM

# Every ``str.splitlines()`` terminator except U+2028, U+2029 and U+0085, which are legal
# unescaped inside a JSON string value. CRLF is matched first, so the pair ends one record
# instead of two.
_RECORD_ENDING = re.compile(r"\r\n|[\n\r\x0b\x0c\x1c-\x1e]")


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


class _LineSplitter:
    """Assembles the record lines of a JSONL body out of the chunks it arrives in.

    The fragments of the line still being assembled are kept as a list and joined once,
    when a record ending finally ends that line. Accumulating them into one string instead
    would copy and re-scan the whole partial record on every chunk, making a record that
    spans many chunks quadratic in its own length.

    A carriage return closing a chunk ends its line as soon as that chunk is fed, rather
    than waiting for the next one, and a line feed opening that next chunk is then dropped
    instead of ending an empty line: a CRLF straddling the boundary stays one ending, and
    no record is held back for a continuation that may never arrive.
    """

    def __init__(self) -> None:
        self._pending: list[str] = []
        self._at_body_start = True
        self._after_carriage_return = False

    def feed(self, chunk: str) -> list[str]:
        """Take the next chunk of the body and return the lines it completes.

        Args:
            chunk: Next non-empty decoded chunk of the body.

        Returns:
            The lines this chunk completes, in arrival order, without their line endings.
        """
        fragment = chunk.removeprefix(UTF8_BOM) if self._at_body_start else chunk
        self._at_body_start = False
        if self._after_carriage_return:
            fragment = fragment.removeprefix("\n")
        self._after_carriage_return = fragment.endswith("\r")
        if not fragment:
            return []
        lines = _RECORD_ENDING.split(fragment)
        trailing = lines.pop()
        if not lines:
            self._pending.append(trailing)
            return []
        self._pending.append(lines[0])
        lines[0] = "".join(self._pending)
        self._pending = [trailing] if trailing else []
        return lines

    def flush(self) -> list[str]:
        """Return the final line when the body ended in the middle of one.

        Returns:
            The unterminated last line, or nothing when the body ended on an ending.
        """
        return ["".join(self._pending)] if self._pending else []


def iter_jsonl_lines(text_chunks: Iterable[str]) -> Iterator[str]:
    """Iterate the lines of a JSONL body, splitting on line-terminating controls.

    A record ends wherever ``str.splitlines()`` ends a line — a carriage return and line
    feed pair, a line feed, a lone carriage return, U+000B, U+000C, or U+001C to U+001E —
    with the three separators that are legal unescaped inside a JSON string value
    excluded: U+2028, U+2029 and U+0085 never split a record, so a text field carrying one
    arrives whole. That exclusion is the only way this differs from ``httpx``'s
    ``iter_lines()``, which it replaces. A single byte order mark opening the body is
    dropped before the first line is formed, and only there: the sibling read paths
    tolerate exactly that one — the paged path's ``json.loads`` on raw bytes strips it,
    and the envelope parser skips it at envelope start — so a BOM-emitting producer parses
    the same in every format.

    Args:
        text_chunks: Decoded text chunks of the body, in arrival order.

    Yields:
        Each line without its line ending — a final unterminated line is yielded as-is,
        and a blank line is yielded as an empty string, for the caller to skip.
    """
    splitter = _LineSplitter()
    for chunk in text_chunks:
        if chunk:
            yield from splitter.feed(chunk)
    yield from splitter.flush()


async def aiter_jsonl_lines(text_chunks: AsyncIterable[str]) -> AsyncIterator[str]:
    """Iterate the lines of an async JSONL body, splitting on line-terminating controls.

    A record ends wherever ``str.splitlines()`` ends a line — a carriage return and line
    feed pair, a line feed, a lone carriage return, U+000B, U+000C, or U+001C to U+001E —
    with the three separators that are legal unescaped inside a JSON string value
    excluded: U+2028, U+2029 and U+0085 never split a record, so a text field carrying one
    arrives whole. That exclusion is the only way this differs from ``httpx``'s
    ``aiter_lines()``, which it replaces. A single byte order mark opening the body is
    dropped before the first line is formed, and only there: the sibling read paths
    tolerate exactly that one — the paged path's ``json.loads`` on raw bytes strips it,
    and the envelope parser skips it at envelope start — so a BOM-emitting producer parses
    the same in every format.

    Args:
        text_chunks: Decoded text chunks of the body, in arrival order.

    Yields:
        Each line without its line ending — a final unterminated line is yielded as-is,
        and a blank line is yielded as an empty string, for the caller to skip.
    """
    splitter = _LineSplitter()
    async for chunk in text_chunks:
        if chunk:
            for line in splitter.feed(chunk):
                yield line
    for line in splitter.flush():
        yield line
