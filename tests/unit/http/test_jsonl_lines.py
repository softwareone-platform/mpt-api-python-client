import asyncio
import json

import pytest

from mpt_api_client.http.jsonl_lines import (
    aiter_jsonl_lines,
    decode_record_line,
    iter_jsonl_lines,
)
from tests.unit.http.conftest import JSON_LEGAL_SEPARATORS, NON_OBJECT_LINE_CASES


async def async_chunks(chunks):
    await asyncio.sleep(0)
    for chunk in chunks:
        yield chunk


@pytest.mark.parametrize("separator", JSON_LEGAL_SEPARATORS)
def test_keeps_json_legal_separator_inline(separator):
    record_line = f'{{"note": "a{separator}b"}}'

    result = list(iter_jsonl_lines([f"{record_line}\n"]))

    assert result == [record_line]


def test_splits_on_crlf():
    result = list(iter_jsonl_lines(['{"id": 1}\r\n{"id": 2}\r\n']))

    assert result == ['{"id": 1}', '{"id": 2}']


def test_reassembles_line_split_across_chunks():
    chunks = ['{"id": ', '"ID-1"}', '\n{"id": "ID-2"}\n']

    result = list(iter_jsonl_lines(chunks))

    assert result == ['{"id": "ID-1"}', '{"id": "ID-2"}']


def test_yields_final_line_without_newline():
    result = list(iter_jsonl_lines(['{"id": 1}\n{"id": 2}']))

    assert result == ['{"id": 1}', '{"id": 2}']


def test_preserves_standalone_trailing_cr():
    result = list(iter_jsonl_lines(['{"id": 1}\r']))

    assert result == ['{"id": 1}\r']


def test_yields_blank_lines_for_caller_to_skip():
    result = list(iter_jsonl_lines(['{"id": 1}\n\n{"id": 2}\n']))

    assert result == ['{"id": 1}', "", '{"id": 2}']


def test_yields_nothing_for_empty_body():
    result = list(iter_jsonl_lines([]))

    assert result == []


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

    result = [line async for line in aiter_jsonl_lines(async_chunks([f"{record_line}\n"]))]

    assert result == [record_line]


async def test_async_splits_on_crlf():
    chunks = async_chunks(['{"id": 1}\r\n{"id": 2}\r\n'])

    result = [line async for line in aiter_jsonl_lines(chunks)]

    assert result == ['{"id": 1}', '{"id": 2}']


async def test_async_reassembles_line_across_chunks():
    chunks = async_chunks(['{"id": ', '"ID-1"}', '\n{"id": "ID-2"}\n'])

    result = [line async for line in aiter_jsonl_lines(chunks)]

    assert result == ['{"id": "ID-1"}', '{"id": "ID-2"}']


async def test_async_yields_final_line_without_newline():
    chunks = async_chunks(['{"id": 1}\n{"id": 2}'])

    result = [line async for line in aiter_jsonl_lines(chunks)]

    assert result == ['{"id": 1}', '{"id": 2}']


async def test_async_preserves_standalone_trailing_cr():
    chunks = async_chunks(['{"id": 1}\r'])

    result = [line async for line in aiter_jsonl_lines(chunks)]

    assert result == ['{"id": 1}\r']
