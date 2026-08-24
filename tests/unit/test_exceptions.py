import json

import pytest
from httpx import HTTPStatusError, Request, Response, codes

from mpt_api_client import exceptions


@pytest.mark.parametrize(
    ("header_value", "received_match"),
    [
        (None, "got no header"),
        ("abc", "got 'abc'"),
    ],
)
def test_item_count_missing_error_message(header_value, received_match):
    result = exceptions.MPTStreamingItemCountMissingError("/api/v1/orders", header_value)

    assert received_match in str(result)


def test_incomplete_error_counts():
    result = exceptions.MPTStreamingIncompleteError("/api/v1/orders", 3, 2)

    assert (result.path, result.expected_count, result.received_count) == (
        "/api/v1/orders",
        3,
        2,
    )


def test_incomplete_error_message():
    error = exceptions.MPTStreamingIncompleteError("/api/v1/orders", 3, 2)

    result = str(error)

    assert result == (
        "The stream for '/api/v1/orders' did not match its declared item count: "
        "the MPT-Item-Count response header declared 3, received 2."
    )


def test_http_error():
    result = exceptions.MPTHttpError(status_code=400, message="Bad request", body="Content")

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

    result = exceptions.MPTAPIError(status_code=status_code, message=message, payload=payload)

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

    result = exceptions.MPTAPIError(status_code=400, message="Bad Request", payload=payload)

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

    result = exceptions.MPTAPIError(status_code=400, message="Bad request", payload=payload)

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

    result = exceptions.MPTAPIError(status_code=400, message="Bad request", payload=payload)

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

    result = exceptions.transform_http_status_exception(exc)

    assert isinstance(result, exceptions.MPTAPIError)
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

    result = exceptions.transform_http_status_exception(exc)

    assert isinstance(result, exceptions.MPTHttpError)
    assert result.status_code == 500
    assert result.body == "Internal Server Error"
    assert str(result) == "HTTP 500: Error message"


def over_cap_problem():
    return {
        "type": "https://api.s1.show/problems/export-too-large",
        "title": "Export too large",
        "status": 413,
        "detail": "the result set exceeds the configured MaxExportKeys of 500000",
        "maxExportKeys": 500000,
    }


def over_cap_message(detail):
    return (
        f"HTTP 413: '/commerce/orders' cannot be exported in one stream: {detail}. "
        "Narrow the filter, set an explicit limit=N, or split the export into key or "
        "date ranges."
    )


def test_over_cap_error_keeps_the_problem_payload():
    result = exceptions.MPTStreamingOverCapError("/commerce/orders", json.dumps(over_cap_problem()))

    assert result.payload == over_cap_problem()
    assert result.path == "/commerce/orders"
    assert result.status_code == codes.REQUEST_ENTITY_TOO_LARGE


def test_over_cap_error_is_streaming_and_http():
    result = exceptions.MPTStreamingOverCapError("/commerce/orders", json.dumps(over_cap_problem()))

    assert isinstance(result, exceptions.MPTStreamingError)
    assert isinstance(result, exceptions.MPTHttpError)


@pytest.mark.parametrize(
    "body",
    [
        pytest.param("", id="empty body"),
        pytest.param("Request Entity Too Large", id="plain text body"),
        pytest.param("[1, 2]", id="json that is not an object"),
    ],
)
def test_over_cap_error_without_a_problem_payload(body):
    result = exceptions.MPTStreamingOverCapError("/commerce/orders", body)

    assert result.payload == {}


@pytest.mark.parametrize(
    ("body", "expected_detail"),
    [
        pytest.param(
            json.dumps(over_cap_problem()),
            "the result set exceeds the configured MaxExportKeys of 500000",
            id="detail taken from the problem+json body",
        ),
        pytest.param(
            "",
            "the result set exceeds the configured cap",
            id="fallback detail when the body carries none",
        ),
    ],
)
def test_over_cap_error_message(body, expected_detail):
    result = exceptions.MPTStreamingOverCapError("/commerce/orders", body)

    assert str(result) == over_cap_message(expected_detail)


def test_raise_streaming_maps_over_cap():
    http_error = exceptions.MPTAPIError(
        status_code=codes.REQUEST_ENTITY_TOO_LARGE,
        message="Content Too Large",
        payload=over_cap_problem(),
    )

    with pytest.raises(exceptions.MPTStreamingOverCapError) as raised:
        exceptions.raise_streaming_error(http_error, "/commerce/orders")

    assert raised.value.payload == over_cap_problem()
    assert raised.value.__cause__ is http_error


def test_streaming_truncated_error():
    result = exceptions.MPTStreamingTruncatedError("/commerce/orders", "peer closed connection")

    assert isinstance(result, exceptions.MPTStreamingError)
    assert result.path == "/commerce/orders"
    assert result.reason == "peer closed connection"


def test_streaming_truncated_error_message():
    error = exceptions.MPTStreamingTruncatedError("/commerce/orders", "peer closed connection")

    result = str(error)  # act

    assert result == (
        "The streaming response for '/commerce/orders' ended before the HTTP message "
        "completed: peer closed connection. The records read so far are an incomplete "
        "snapshot; discard them and restart the export from scratch."
    )
