import json

import pytest

from mpt_api_client.http.json_envelope_parser import (
    JSONEnvelopeParser,
    StreamedRecord,
    StreamedTotal,
    reported_total,
)

FIRST_RECORD_JSON = '{"id": "ID-1", "name": "Order 1"}'
SECOND_RECORD_JSON = '{"id": "ID-2", "name": "Order 2"}'
UNTERMINATED_MATCH = "Unterminated JSON envelope"
META_JSON = '"$meta": {"pagination": {"total": 2}}'
SPLIT_TOTAL = 1234
# Every token kind a split can land inside: an escaped string, numbers with fraction and
# exponent, the literals, and nested containers around the record array.
SPLIT_SWEEP_BODY = (
    r'{"$meta": {"pagination": {"total": 2}}, "ignored": ["a\u00e9\n", -1.5e-3, true, null],'
    f' "data": [{FIRST_RECORD_JSON}, {SECOND_RECORD_JSON}]}}'
)


@pytest.fixture
def parse_envelope():
    def factory(chunks, data_field="data"):
        parser = JSONEnvelopeParser(data_field)
        events = [event for chunk in chunks for event in parser.feed(chunk)]
        parser.close()
        return events

    return factory


@pytest.fixture
def first_event():
    return StreamedRecord(json.loads(FIRST_RECORD_JSON))


@pytest.fixture
def second_event():
    return StreamedRecord(json.loads(SECOND_RECORD_JSON))


@pytest.fixture
def envelope_body():
    return f'{{{META_JSON}, "data": [{FIRST_RECORD_JSON}, {SECOND_RECORD_JSON}]}}'


def test_parses_a_whole_envelope_in_one_chunk(
    parse_envelope, envelope_body, first_event, second_event
):
    result = parse_envelope([envelope_body])

    assert result == [
        StreamedTotal(2),
        first_event,
        second_event,
    ]


def test_emits_a_record_before_the_body_ends(first_event):
    parser = JSONEnvelopeParser()

    result = list(parser.feed(f'{{"data": [{FIRST_RECORD_JSON},'))  # act

    assert result == [first_event]


def test_emits_one_record_per_arriving_chunk():
    chunks = ['{"data": [', FIRST_RECORD_JSON, ",", SECOND_RECORD_JSON, "]}"]
    parser = JSONEnvelopeParser()
    fed = [list(parser.feed(chunk)) for chunk in chunks]

    result = [len(events) for events in fed]  # act

    assert result == [0, 1, 0, 1, 0]


@pytest.mark.parametrize(
    "chunks",
    [
        pytest.param(
            ['{"$meta": {"pagi', 'nation": {"total": 2}}, "data": [{"id": "ID-1", "name": '],
            id="split inside a member name and before a value",
        ),
        pytest.param(
            ['{"$meta": {"pagination": {"total": 2}}, "data": [{"id": "ID-1", "na', 'me": '],
            id="split inside a record",
        ),
    ],
)
def test_records_survive_chunk_splits(parse_envelope, chunks, first_event, second_event):
    tail = ['"Order 1"}, ', SECOND_RECORD_JSON, "]}"]

    result = parse_envelope(chunks + tail)

    assert result == [
        StreamedTotal(2),
        first_event,
        second_event,
    ]


def test_split_total_arrives_whole(parse_envelope):
    chunks = ['{"$meta": {"pagination": {"total": 12', '34}}, "data": []}']

    result = parse_envelope(chunks)

    assert result == [StreamedTotal(SPLIT_TOTAL)]


@pytest.mark.parametrize(
    ("head", "tail"),
    [
        pytest.param('{"ignoredCount": 12', "34", id="integer - decoder stops at the end"),
        pytest.param('{"elapsed": 12.', "34", id="fraction - decoder stops before the point"),
        pytest.param('{"elapsed": 1e', "3", id="exponent - decoder stops before the e"),
    ],
)
def test_split_number_is_not_read_early(parse_envelope, first_event, head, tail):
    # A number is the one token a later chunk can extend, and raw_decode reads the longest
    # prefix it can, so a value split at the boundary must wait rather than decode to that
    # prefix — including a fraction or exponent, where the decoder stops before the leftover
    # character rather than at the buffer end.
    chunks = [head, f'{tail}, "data": [{FIRST_RECORD_JSON}]}}']

    result = parse_envelope(chunks)

    assert result == [first_event]


def test_consumes_whitespace_keepalives(parse_envelope, first_event, second_event):
    chunks = [
        "  ",
        '{"data"',
        " \n ",
        ":",
        "\n\n",
        "[",
        " ",
        FIRST_RECORD_JSON,
        " \t ",
        ",",
        "\r\n",
        SECOND_RECORD_JSON,
        "\n",
        "]",
        " \n ",
        "}",
        "\n",
    ]

    result = parse_envelope(chunks)

    assert result == [first_event, second_event]


def test_reports_the_total_after_the_records(parse_envelope, first_event):
    body = f'{{"data": [{FIRST_RECORD_JSON}], "$meta": {{"pagination": {{"total": 1}}}}}}'

    result = parse_envelope([body])

    assert result == [first_event, StreamedTotal(1)]


def test_reads_records_from_the_configured_member(parse_envelope, first_event):
    body = f'{{"items": [{FIRST_RECORD_JSON}]}}'

    result = parse_envelope([body], "items")

    assert result == [first_event]


@pytest.mark.parametrize(
    "body",
    [
        pytest.param('{"data": []}', id="empty record array"),
        pytest.param("{}", id="empty envelope"),
        pytest.param('{"data": [], "$meta": {}}', id="$meta without pagination"),
        pytest.param('{"data": [], "$meta": {"pagination": {}}}', id="pagination without total"),
        pytest.param(
            '{"data": [], "$meta": {"pagination": {"total": "2"}}}', id="total not a number"
        ),
        pytest.param('{"data": [], "$meta": {"pagination": {"total": true}}}', id="total is true"),
        pytest.param('{"data": [], "$meta": {"pagination": {"total": -1}}}', id="total negative"),
        pytest.param('{"data": [], "$meta": {"pagination": []}}', id="pagination not an object"),
        pytest.param('{"data": [], "$meta": "deleted"}', id="$meta not an object"),
        pytest.param('{"data": [], "ignored": ["name"]}', id="unknown member"),
    ],
)
def test_empty_envelopes_emit_nothing(parse_envelope, body):
    result = parse_envelope([body])

    assert result == []


@pytest.mark.parametrize(
    ("chunks", "error_match"),
    [
        pytest.param(['{"data": [{"id": "ID-1"}'], UNTERMINATED_MATCH, id="array left open"),
        pytest.param(['{"data": [{"id": '], "Expecting value", id="record left open"),
        pytest.param([""], UNTERMINATED_MATCH, id="empty body"),
    ],
)
def test_close_rejects_an_unclosed_envelope(chunks, error_match):
    parser = JSONEnvelopeParser()
    for chunk in chunks:
        list(parser.feed(chunk))

    with pytest.raises(json.JSONDecodeError, match=error_match):
        parser.close()


@pytest.mark.parametrize(
    ("body", "error_match"),
    [
        pytest.param("[]", "Expected '{'", id="not an object"),
        pytest.param("{1: 2}", "member name must be a string", id="member name not a string"),
        pytest.param('{"data" 1}', "Expected ':'", id="colon missing"),
        pytest.param('{"data": 1}', r"Expected '\['", id="record member not an array"),
        pytest.param('{"data": [1]}', "record must be an object", id="record not an object"),
        pytest.param('{"data": [{} {}]}', r"Expected ',' or '\]'", id="element separator missing"),
        pytest.param('{"data": [] "x": 1}', r"Expected ',' or '}'", id="member separator missing"),
        pytest.param('{"data": [}]', "found '}'", id="delimiter where a record must start"),
        pytest.param('{"data": [,1]', "found ','", id="comma where a record must start"),
        pytest.param('{"data": []}garbage', "Trailing content", id="suffix after the envelope"),
        pytest.param('{"data": []}{"data": []}', "Trailing content", id="a second envelope"),
    ],
)
def test_feed_rejects_a_malformed_envelope(body, error_match):
    parser = JSONEnvelopeParser()

    with pytest.raises(json.JSONDecodeError, match=error_match):
        list(parser.feed(body))


@pytest.mark.parametrize(
    ("body", "error_match"),
    [
        pytest.param(
            '{"data": [{"id" "x"}]}', "Expecting ':' delimiter", id="record missing a colon"
        ),
        pytest.param('{"x": nulx, "data": []}', "Expecting value", id="broken literal"),
        pytest.param('{"x": -, "data": []}', "Expecting value", id="minus without digits"),
        pytest.param(
            '{"x": [1 2], "data": []}', "Expecting ',' delimiter", id="separator lost in a value"
        ),
        pytest.param(r'{"x": "a\q", "data": []}', r"Invalid \\escape", id="broken escape"),
        pytest.param(
            '{"x": "a\x01b", "data": []}', "Invalid control character", id="control character"
        ),
        pytest.param(
            r'{"x": "a\u12G8", "data": []}', r"Invalid \\uXXXX escape", id="broken unicode escape"
        ),
        pytest.param(
            r'{"x": "a\u1G', r"Invalid \\uXXXX escape", id="unicode escape broken at the boundary"
        ),
    ],
)
def test_feed_rejects_an_undecodable_value(body, error_match):
    # A value that can never decode however much body follows must be rejected at the
    # chunk that proves it, not buffered until close() — the decoder's own error is the
    # precise diagnosis.
    parser = JSONEnvelopeParser()

    with pytest.raises(json.JSONDecodeError, match=error_match):
        list(parser.feed(body))


@pytest.mark.parametrize(
    "chunks",
    [
        pytest.param(
            ['{"x": nul', f'l, "data": [{FIRST_RECORD_JSON}]}}'],
            id="literal split at the boundary",
        ),
        pytest.param(
            ['{"x": -', f'1, "data": [{FIRST_RECORD_JSON}]}}'],
            id="number split after its minus sign",
        ),
        pytest.param(
            [r'{"x": "a\u00', f'e9", "data": [{FIRST_RECORD_JSON}]}}'],
            id="unicode escape split between its digits",
        ),
        pytest.param(
            ['{"x": [1.', f'5], "data": [{FIRST_RECORD_JSON}]}}'],
            id="nested number split inside its fraction",
        ),
    ],
)
def test_split_values_stay_in_flight(parse_envelope, chunks, first_event):
    result = parse_envelope(chunks)

    assert result == [first_event]


def test_split_points_parse_like_the_whole_body(parse_envelope):
    expected = parse_envelope([SPLIT_SWEEP_BODY])

    result = [
        split
        for split in range(1, len(SPLIT_SWEEP_BODY))
        if parse_envelope([SPLIT_SWEEP_BODY[:split], SPLIT_SWEEP_BODY[split:]]) != expected
    ]

    assert result == []


def test_close_accepts_a_terminated_envelope(
    parse_envelope, envelope_body, first_event, second_event
):
    result = parse_envelope([envelope_body, "\n \n"])

    assert result == [
        StreamedTotal(2),
        first_event,
        second_event,
    ]


@pytest.mark.parametrize(
    "value_start",
    [
        pytest.param('"', id="string"),
        pytest.param("{", id="object"),
        pytest.param("[", id="array"),
        pytest.param("-", id="negative number"),
        pytest.param("1", id="number"),
        pytest.param("t", id="true"),
        pytest.param("f", id="false"),
        pytest.param("n", id="null"),
    ],
)
def test_feed_waits_for_a_value_in_flight(value_start):
    # The other half of failing fast: every character a JSON value can begin with must
    # still be treated as a token in flight, however little of it has arrived.
    parser = JSONEnvelopeParser()

    result = list(parser.feed(f'{{"data": [{value_start}'))  # act

    assert result == []


def test_rejects_a_suffix_in_a_later_chunk(envelope_body):
    parser = JSONEnvelopeParser()
    list(parser.feed(envelope_body))

    with pytest.raises(json.JSONDecodeError, match="Trailing content"):
        list(parser.feed("garbage"))


def test_reported_total_reads_the_total():
    result = reported_total({"pagination": {"total": 2}})

    assert result == StreamedTotal(2)
