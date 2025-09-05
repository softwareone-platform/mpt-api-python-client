import pytest
from httpx import Response

from mpt_api_client.models import FileModel


@pytest.fixture
def empty_file():
    return FileModel(Response(200))


def test_download_file_init():
    response = Response(200)
    download_file = FileModel(response)

    assert download_file.response == response


def test_filename(empty_file):
    empty_file.response.headers["content-disposition"] = 'attachment; filename="test.pdf"'

    filename = empty_file.filename

    assert filename == "test.pdf"


def test_filename_with_utf8_format(empty_file):
    empty_file.response.headers["content-disposition"] = (
        "attachment; filename*=UTF-8''test%20file.pdf"
    )

    filename = empty_file.filename

    assert filename == "test%20file.pdf"


def test_filename_without_quotes():
    response = Response(200)
    response.headers["content-disposition"] = "attachment; filename=test.pdf"
    download_file = FileModel(response)

    filename = download_file.filename

    assert filename == "test.pdf"


def test_filename_case_insensitive(empty_file):
    empty_file.response.headers["content-disposition"] = 'ATTACHMENT; FILENAME="test.pdf"'

    assert empty_file.filename == "test.pdf"


def test_filename_no_content_disposition(empty_file):
    filename = empty_file.filename

    assert filename is None


def test_filename_empty_content_disposition(empty_file):
    empty_file.response.headers["content-disposition"] = ""

    assert empty_file.filename is None


def test_filename_no_filename_in_header():
    response = Response(200)
    response.headers["content-disposition"] = "attachment"
    download_file = FileModel(response)

    filename = download_file.filename

    assert filename is None


def test_file_contents():
    response = Response(200, content=b"test content")
    download_file = FileModel(response)

    assert download_file.file_contents == b"test content"


def test_content_type():
    response = Response(200)
    response.headers["content-type"] = "application/pdf"
    download_file = FileModel(response)

    assert download_file.content_type == "application/pdf"


def test_content_type_none():
    response = Response(200)
    download_file = FileModel(response)

    assert not download_file.content_type
