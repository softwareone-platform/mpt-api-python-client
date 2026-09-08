import asyncio
import json
import re
import time
from pathlib import Path
from typing import NamedTuple

import pytest

import mpt_api_client
from mpt_api_client.http.jsonl_lines import (
    aiter_jsonl_lines,
    decode_record_line,
    iter_jsonl_lines,
)
from tests.unit.http.conftest import (
    JSON_LEGAL_SEPARATORS,
    NON_OBJECT_LINE_CASES,
    RECORD_TERMINATORS,
)

PACKAGE_ROOT = Path(mpt_api_client.__file__).parent
HTTPX_LINE_ITERATOR_CALL = re.compile(r"\.a?iter_lines\(")

# Chunkings that must still yield the same two records: the framing decisions live at the
# chunk boundary, where an ending can arrive alone or be split down the middle.
TWO_RECORD_CHUNKINGS = (
    pytest.param(['{"id": 1}', "\r\n", '{"id": 2}'], id="ending in its own chunk"),
    pytest.param(['{"id": 1}\r', '\n{"id": 2}\n'], id="CRLF straddling a boundary"),
    pytest.param(['{"id": 1}\r', '{"id": 2}\n'], id="chunk-trailing CR alone"),
    pytest.param(['{"id": 1}\n{"id": 2}'], id="unterminated final line"),
)

# A single byte order mark opening the body is dropped however the body is chunked.
LEADING_BOM_CHUNKINGS = (
    pytest.param(['﻿{"id": 1}\n'], id="BOM opening the first chunk"),
    pytest.param(["﻿", '{"id": 1}\n'], id="BOM in its own chunk"),
    pytest.param(["", '﻿{"id": 1}\n'], id="BOM after an empty chunk"),
)


async def async_chunks(chunks):
    await asyncio.sleep(0)
    for chunk in chunks:
        yield chunk


@pytest.mark.parametrize("separator", JSON_LEGAL_SEPARATORS)
def test_keeps_json_legal_separator_inline(separator):
    record_line = f'{{"note": "a{separator}b"}}'

    result = list(iter_jsonl_lines([f"{record_line}\n"]))

    assert result == [record_line]


@pytest.mark.parametrize("terminator", RECORD_TERMINATORS)
def test_splits_on_every_record_terminator(terminator):
    body = f'{{"id": 1}}{terminator}{{"id": 2}}{terminator}'

    result = list(iter_jsonl_lines([body]))

    assert result == ['{"id": 1}', '{"id": 2}']


@pytest.mark.parametrize("terminator", RECORD_TERMINATORS)
def test_matches_splitlines_on_terminator(terminator):
    body = f'{{"id": 1}}{terminator}{{"id": 2}}{terminator}'

    result = list(iter_jsonl_lines([body]))

    assert result == body.splitlines()


@pytest.mark.parametrize("chunks", TWO_RECORD_CHUNKINGS)
def test_splits_records_across_chunk_boundaries(chunks):
    result = list(iter_jsonl_lines(chunks))

    assert result == ['{"id": 1}', '{"id": 2}']


def test_reassembles_line_split_across_chunks():
    chunks = ['{"id": ', '"ID-1"}', '\n{"id": "ID-2"}\n']

    result = list(iter_jsonl_lines(chunks))

    assert result == ['{"id": "ID-1"}', '{"id": "ID-2"}']


def test_ends_final_line_on_trailing_cr():
    result = list(iter_jsonl_lines(['{"id": 1}\r']))

    assert result == ['{"id": 1}']


def test_yields_blank_lines_for_caller_to_skip():
    result = list(iter_jsonl_lines(['{"id": 1}\n\n{"id": 2}\n']))

    assert result == ['{"id": 1}', "", '{"id": 2}']


def test_yields_nothing_for_empty_body():
    result = list(iter_jsonl_lines([]))

    assert result == []


@pytest.mark.parametrize("chunks", LEADING_BOM_CHUNKINGS)
def test_drops_a_byte_order_mark_opening_the_body(chunks):
    result = list(iter_jsonl_lines(chunks))

    assert result == ['{"id": 1}']


def test_drops_only_one_leading_bom():
    # json.loads on raw bytes strips a single BOM, so a second one still fails decode.
    doubled_bom_body = '﻿﻿{"id": 1}\n'

    result = list(iter_jsonl_lines([doubled_bom_body]))

    assert result == ['﻿{"id": 1}']


def test_keeps_a_bom_after_the_body_start():
    result = list(iter_jsonl_lines(['{"id": 1}\n﻿{"id": 2}\n']))

    assert result == ['{"id": 1}', '﻿{"id": 2}']


LONG_RECORD_CHUNK_SIZE = 8 * 1024
LONG_RECORD_SIZE = 16 * 1024 * 1024
# The linear splitter needs a few milliseconds for a 16MB record, while re-splitting the
# whole buffer on every chunk needed seconds, so this budget is generous on a slow
# machine and still fails on a return to quadratic behaviour.
LONG_RECORD_BUDGET_SECONDS = 2


@pytest.fixture(scope="module")
def long_record():
    # Built on demand rather than at import, so runs that do not select the tests below
    # do not pay for the 16MB body during collection.
    return json.dumps({"note": "a" * LONG_RECORD_SIZE})


def chunked(body, size=LONG_RECORD_CHUNK_SIZE):
    offsets = range(0, len(body), size)
    return [body[offset : offset + size] for offset in offsets]


class TimedLines(NamedTuple):
    lines: list[str]
    elapsed: float


def timed_lines(chunks):
    started_at = time.perf_counter()
    lines = list(iter_jsonl_lines(chunks))
    return TimedLines(lines, time.perf_counter() - started_at)


async def collected_lines(chunks):
    return [line async for line in aiter_jsonl_lines(chunks)]


async def timed_async_lines(chunks):
    started_at = time.perf_counter()
    lines = await collected_lines(chunks)
    return TimedLines(lines, time.perf_counter() - started_at)


def test_long_record_across_chunks_is_linear(long_record):
    chunks = chunked(f"{long_record}\n")

    result = timed_lines(chunks)

    assert result.lines == [long_record]
    assert result.elapsed < LONG_RECORD_BUDGET_SECONDS


def test_unterminated_long_record_is_linear(long_record):
    # The body confirm_stream_format tolerates without a content type: a single long
    # line, unterminated, so every chunk stays buffered and nothing is flushed early.
    chunks = chunked(long_record)

    result = timed_lines(chunks)

    assert result.lines == [long_record]
    assert result.elapsed < LONG_RECORD_BUDGET_SECONDS


def test_decode_record_line_returns_the_object():
    result = decode_record_line('{"id": "ID-1"}')

    assert result == {"id": "ID-1"}


@pytest.mark.parametrize("line", NON_OBJECT_LINE_CASES)
def test_decode_record_line_rejects_non_object(line):
    with pytest.raises(json.JSONDecodeError, match="record must be an object"):
        decode_record_line(line)


@pytest.mark.parametrize("separator", JSON_LEGAL_SEPARATORS)
async def test_async_keeps_json_legal_separator_inline(separator):
    record_line = f'{{"note": "a{separator}b"}}'

    result = await collected_lines(async_chunks([f"{record_line}\n"]))

    assert result == [record_line]


@pytest.mark.parametrize("terminator", RECORD_TERMINATORS)
async def test_async_splits_on_every_record_terminator(terminator):
    body = f'{{"id": 1}}{terminator}{{"id": 2}}{terminator}'

    result = await collected_lines(async_chunks([body]))

    assert result == body.splitlines()


@pytest.mark.parametrize("chunks", TWO_RECORD_CHUNKINGS)
async def test_async_splits_records_across_boundaries(chunks):
    result = await collected_lines(async_chunks(chunks))

    assert result == ['{"id": 1}', '{"id": 2}']


async def test_async_reassembles_line_across_chunks():
    chunks = async_chunks(['{"id": ', '"ID-1"}', '\n{"id": "ID-2"}\n'])

    result = await collected_lines(chunks)

    assert result == ['{"id": "ID-1"}', '{"id": "ID-2"}']


async def test_async_ends_final_line_on_trailing_cr():
    chunks = async_chunks(['{"id": 1}\r'])

    result = await collected_lines(chunks)

    assert result == ['{"id": 1}']


async def test_async_long_record_is_linear(long_record):
    chunks = async_chunks(chunked(f"{long_record}\n"))

    result = await timed_async_lines(chunks)

    assert result.lines == [long_record]
    assert result.elapsed < LONG_RECORD_BUDGET_SECONDS


@pytest.mark.parametrize("chunks", LEADING_BOM_CHUNKINGS)
async def test_async_drops_a_bom_opening_the_body(chunks):
    result = await collected_lines(async_chunks(chunks))

    assert result == ['{"id": 1}']


def test_package_never_calls_httpx_iter_lines():
    """No JSONL reader may go back to the response's own line iterator.

    It follows ``str.splitlines()``, so it breaks a record at U+2028, U+2029 or U+0085 -
    the defect these helpers exist to avoid. Naming it in prose stays allowed; calling it
    does not, so a new reader cannot reintroduce the fracture unnoticed.
    """
    sources = sorted(PACKAGE_ROOT.rglob("*.py"))

    result = [
        str(source.relative_to(PACKAGE_ROOT))
        for source in sources
        if HTTPX_LINE_ITERATOR_CALL.search(source.read_text(encoding="utf-8"))
    ]

    assert result == []
