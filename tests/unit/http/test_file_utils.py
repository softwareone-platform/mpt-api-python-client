import io
import os

import pytest

from mpt_api_client.http.file_utils import declare_content_type

NDJSON = "application/x-ndjson"
CSV = "text/csv"


@pytest.mark.parametrize(
    ("file_part", "expected"),
    [
        pytest.param(
            b'{"id": 1}\n',
            ("upload", b'{"id": 1}\n', NDJSON),
            id="bytes without a name",
        ),
        pytest.param(
            ("journal.jsonl", b'{"id": 1}\n'),
            ("journal.jsonl", b'{"id": 1}\n', NDJSON),
            id="filename and content",
        ),
        pytest.param(
            ("journal.jsonl", b'{"id": 1}\n', None),
            ("journal.jsonl", b'{"id": 1}\n', NDJSON),
            id="content type left unset",
        ),
        pytest.param(
            ("journal.jsonl", b'{"id": 1}\n', CSV),
            ("journal.jsonl", b'{"id": 1}\n', CSV),
            id="content type declared by the caller",
        ),
        pytest.param(
            ("journal.jsonl", b'{"id": 1}\n', ""),
            ("journal.jsonl", b'{"id": 1}\n', NDJSON),
            id="blank content type treated as absent",
        ),
        pytest.param(
            ("journal.jsonl", b'{"id": 1}\n', None, {"X-Trace": "1"}),
            ("journal.jsonl", b'{"id": 1}\n', NDJSON, {"X-Trace": "1"}),
            id="extra headers preserved",
        ),
        pytest.param(
            (None, b'{"id": 1}\n'),
            (None, b'{"id": 1}\n', NDJSON),
            id="form field without a filename",
        ),
    ],
)
def test_declare_content_type(file_part, expected):
    result = declare_content_type(file_part, NDJSON)

    assert result == expected


def test_filename_taken_from_file_object(tmp_path):
    file_path = tmp_path / "journal.jsonl"
    file_path.write_bytes(b'{"id": 1}\n')

    with file_path.open("rb") as file_obj:
        result = declare_content_type(file_obj, NDJSON)

        assert result == ("journal.jsonl", file_obj, NDJSON)


def test_filename_falls_back_without_name():
    file_obj = io.BytesIO(b'{"id": 1}\n')

    result = declare_content_type(file_obj, NDJSON)

    assert result == ("upload", file_obj, NDJSON)


def test_filename_from_file_descriptor(tmp_path):
    file_path = tmp_path / "journal.jsonl"
    file_path.write_bytes(b'{"id": 1}\n')
    descriptor = os.open(file_path, os.O_RDONLY)

    with os.fdopen(descriptor, "rb") as file_obj:
        result = declare_content_type(file_obj, NDJSON)

        assert result == (str(descriptor), file_obj, NDJSON)
