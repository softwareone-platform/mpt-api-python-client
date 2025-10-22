import json

from httpx import HTTPStatusError, Request, Response

from mpt_api_client.exceptions import (
    MPTAPIError,
    MPTHttpError,
    transform_http_status_exception,
)


def test_http_error():
    exception = MPTHttpError(status_code=400, message="Bad request", body="Content")

    assert exception.status_code == 400
    assert exception.body == "Content"
    assert str(exception) == "HTTP 400: Bad request"


def test_http_error_not_found_from_mpt():  # noqa: WPS218
    status_code = 400  # changed from 404 for testing purposes
    api_status_code = 404
    payload = {"message": "Resource not found", "statusCode": api_status_code}
    message = (
        "Client error '404 Resource Not Found' for url "
        "'https://api.s1.show/public/public/v1/catalog/products?limit=100&offset=0'\n"
        "For more information check: "
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404"
    )

    exception = MPTAPIError(status_code=status_code, message=message, payload=payload)

    assert exception.status_code == status_code
    assert exception.payload == payload
    assert exception.status == api_status_code
    assert exception.title == "Resource not found"
    assert exception.detail == message
    assert exception.trace_id is None
    assert exception.errors is None
    assert str(exception) == f"404 Resource not found - {message} (no-trace-id)"


def test_api_error():  # noqa: WPS218
    payload = {
        "status": "400",
        "title": "Bad Request",
        "detail": "Invalid input",
        "traceId": "abc123",
        "errors": "Some error details",
    }
    exception = MPTAPIError(status_code=400, message="Bad Request", payload=payload)

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
    exception = MPTAPIError(status_code=400, message="Bad request", payload=payload)

    assert str(exception) == '400 Bad Request - Invalid input (abc123)\n"Some error details"'
    assert repr(exception) == (
        "{'status': '400', 'title': 'Bad Request', 'detail': 'Invalid input', "
        "'traceId': 'abc123', 'errors': 'Some error details'}"
    )


def test_api_error_str_no_errors():
    payload = {
        "status": "400",
        "title": "Bad Request",
        "detail": "Invalid input",
        "traceId": "abc123",
    }

    exception = MPTAPIError(status_code=400, message="Bad request", payload=payload)

    assert str(exception) == "400 Bad Request - Invalid input (abc123)"


def test_transform_http_status_exception_api():
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


def test_transform_http_status_exception():
    response = Response(
        status_code=500,
        request=Request("GET", "http://test"),
        content=b"Internal Server Error",
        headers={"content-type": "text/plain"},
    )
    exc = HTTPStatusError("Error message", request=response.request, response=response)

    err = transform_http_status_exception(exc)

    assert isinstance(err, MPTHttpError)
    assert err.status_code == 500
    assert err.body == "Internal Server Error"
    assert str(err) == "HTTP 500: Error message"
