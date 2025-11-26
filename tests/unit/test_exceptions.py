import json

from httpx import HTTPStatusError, Request, Response

from mpt_api_client.exceptions import (
    MPTAPIError,
    MPTHttpError,
    transform_http_status_exception,
)


def test_http_error():
    result = MPTHttpError(status_code=400, message="Bad request", body="Content")

    assert result.status_code == 400
    assert result.body == "Content"
    assert str(result) == "HTTP 400: Bad request"


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

    result = MPTAPIError(status_code=status_code, message=message, payload=payload)

    assert result.status_code == status_code
    assert result.payload == payload
    assert result.status == api_status_code
    assert result.title == "Resource not found"
    assert result.detail == message
    assert result.trace_id is None
    assert result.errors is None
    assert str(result) == f"404 Resource not found - {message} (no-trace-id)"


def test_api_error():  # noqa: WPS218
    payload = {
        "status": "400",
        "title": "Bad Request",
        "detail": "Invalid input",
        "traceId": "abc123",
        "errors": "Some error details",
    }

    result = MPTAPIError(status_code=400, message="Bad Request", payload=payload)

    assert result.status_code == 400
    assert result.payload == payload
    assert result.status == "400"
    assert result.title == "Bad Request"
    assert result.detail == "Invalid input"
    assert result.trace_id == "abc123"
    assert result.errors == "Some error details"


def test_api_error_str_and_repr():
    payload = {
        "status": "400",
        "title": "Bad Request",
        "detail": "Invalid input",
        "traceId": "abc123",
        "errors": "Some error details",
    }

    result = MPTAPIError(status_code=400, message="Bad request", payload=payload)

    assert str(result) == '400 Bad Request - Invalid input (abc123)\n"Some error details"'
    assert repr(result) == (
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

    result = MPTAPIError(status_code=400, message="Bad request", payload=payload)

    assert str(result) == "400 Bad Request - Invalid input (abc123)"


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

    result = transform_http_status_exception(exc)

    assert isinstance(result, MPTAPIError)
    assert result.status_code == 400
    assert result.payload == payload


def test_transform_http_status_exception():
    response = Response(
        status_code=500,
        request=Request("GET", "http://test"),
        content=b"Internal Server Error",
        headers={"content-type": "text/plain"},
    )
    exc = HTTPStatusError("Error message", request=response.request, response=response)

    result = transform_http_status_exception(exc)

    assert isinstance(result, MPTHttpError)
    assert result.status_code == 500
    assert result.body == "Internal Server Error"
    assert str(result) == "HTTP 500: Error message"
