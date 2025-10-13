import json

from httpx import HTTPStatusError, Request, Response

from mpt_api_client.exceptions import (
    MPTAPIError,
    MPTHttpError,
    transform_http_status_exception,
)


def test_http_error():
    exception = MPTHttpError(status_code=400, text="Content")

    assert exception.status_code == 400
    assert exception.text == "Content"


def test_api_error():  # noqa: WPS218
    payload = {
        "status": "400",
        "title": "Bad Request",
        "detail": "Invalid input",
        "traceId": "abc123",
        "errors": "Some error details",
    }
    exception = MPTAPIError(status_code=400, payload=payload)

    assert exception.status_code == 400
    assert exception.payload == payload
    assert exception.status == "400"
    assert exception.title == "Bad Request"
    assert exception.detail == "Invalid input"
    assert exception.trace_id == "abc123"
    assert exception.errors == "Some error details"


def test_api_error_str_and_repr():
    payload = {
        "status": "400",
        "title": "Bad Request",
        "detail": "Invalid input",
        "traceId": "abc123",
        "errors": "Some error details",
    }
    exception = MPTAPIError(status_code=400, payload=payload)

    assert str(exception) == '400 Bad Request - Invalid input (abc123)\n"Some error details"'
    assert repr(exception) == (
        "{'status': '400', 'title': 'Bad Request', 'detail': 'Invalid input', "
        "'traceId': 'abc123', 'errors': 'Some error details'}"
    )


def test_transform_http_status_exception():
    payload = {
        "status": "400",
        "title": "Bad Request",
        "detail": "Invalid input",
        "traceId": "abc123",
        "errors": "Some error details",
    }
    response = Response(
        status_code=400,
        request=Request("GET", "http://test"),
        content=json.dumps(payload).encode(),
        headers={"content-type": "application/json"},
    )
    exc = HTTPStatusError("error", request=response.request, response=response)

    err = transform_http_status_exception(exc)

    assert isinstance(err, MPTAPIError)
    assert err.status_code == 400
    assert err.payload == payload


def test_transform_http_status_exception_json():
    response = Response(
        status_code=500,
        request=Request("GET", "http://test"),
        content=b"Internal Server Error",
        headers={"content-type": "text/plain"},
    )
    exc = HTTPStatusError("error", request=response.request, response=response)

    err = transform_http_status_exception(exc)

    assert isinstance(err, MPTHttpError)
    assert err.status_code == 500
    assert err.text == "Internal Server Error"
