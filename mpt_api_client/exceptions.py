import json
from typing import NoReturn, override

from httpx import HTTPStatusError, codes

from mpt_api_client.constants import (
    MPT_ITEM_COUNT_HEADER,
    MPT_STREAMING_ENABLED,
    MPT_STREAMING_HEADER,
)

STREAMING_NOT_ACCEPTABLE_STATUS = codes.NOT_ACCEPTABLE
STREAMING_NOT_IMPLEMENTED_STATUS = codes.NOT_IMPLEMENTED


class MPTError(Exception):
    """Represents a generic MPT error."""


class MPTStreamingError(MPTError):
    """Base class for failures specific to the streaming read mode."""


class MPTStreamingNotEnabledError(MPTStreamingError):
    """Represents a streaming request the API did not answer in streaming mode.

    The API confirms streaming mode by echoing the ``MPT-Streaming`` response header.
    Without that confirmation the body is a regular paged response, and consuming it as
    a stream would yield a silently incomplete result, so the response is not read.
    """

    def __init__(self, path: str, echoed_value: str | None):
        self.path = path
        self.echoed_value = echoed_value
        received = "no header" if echoed_value is None else f"'{echoed_value}'"
        super().__init__(
            f"The API did not confirm streaming mode for '{path}': expected the "
            f"{MPT_STREAMING_HEADER} response header to be '{MPT_STREAMING_ENABLED}', "
            f"got {received}. The response body was not consumed."
        )


class MPTStreamingItemCountMissingError(MPTStreamingError):
    """Represents a streaming response that did not declare a usable item count.

    Streaming mode commits the ``MPT-Item-Count`` response header together with the
    status, and it is the only completeness signal the contract provides. Without a
    usable count the stream cannot be verified complete, so the response is not read.
    """

    def __init__(self, path: str, header_value: str | None):
        self.path = path
        self.header_value = header_value
        received = "no header" if header_value is None else f"'{header_value}'"
        super().__init__(
            f"The API did not declare the item count for '{path}': expected the "
            f"{MPT_ITEM_COUNT_HEADER} response header to be a non-negative integer, "
            f"got {received}. The response body was not consumed."
        )


class MPTStreamingIncompleteError(MPTStreamingError):
    """Represents a fully consumed stream that did not match its declared item count.

    Every member of the export yields exactly one record, so a gracefully terminated
    stream whose record count differs from ``MPT-Item-Count`` is an incomplete or
    duplicated result set and must not be processed as if it were complete.
    """

    def __init__(self, path: str, expected_count: int, received_count: int):
        self.path = path
        self.expected_count = expected_count
        self.received_count = received_count
        super().__init__(
            f"The stream for '{path}' did not match its declared item count: the "
            f"{MPT_ITEM_COUNT_HEADER} response header declared {expected_count}, "
            f"received {received_count}."
        )


class MPTHttpError(MPTError):
    """Represents an HTTP error."""

    def __init__(self, status_code: int, message: str, body: str):
        self.status_code = status_code
        self.body = body
        super().__init__(f"HTTP {status_code}: {message}")


class MPTStreamingNotSupportedError(MPTStreamingError, MPTHttpError):
    """Represents a resource whose query service cannot stream.

    The API answers ``501`` when the resource provides no streaming-capable execution
    strategy, rather than silently degrading to a buffered read. Use ``iterate()`` for
    such resources.
    """

    def __init__(self, path: str, body: str):
        self.path = path
        MPTHttpError.__init__(
            self,
            STREAMING_NOT_IMPLEMENTED_STATUS,
            f"'{path}' does not support streaming mode: the resource provides no "
            "streaming-capable execution strategy. Use iterate() instead.",
            body,
        )


class MPTStreamingNotAcceptableError(MPTStreamingError, MPTHttpError):
    """Represents a streaming request whose requested format the API cannot serve.

    The API answers ``406`` when the ``Accept`` header cannot be satisfied for the
    requested read mode.
    """

    def __init__(self, path: str, body: str):
        self.path = path
        MPTHttpError.__init__(
            self,
            STREAMING_NOT_ACCEPTABLE_STATUS,
            f"'{path}' cannot serve the requested streaming format. Check the Accept "
            "header against the formats the endpoint negotiates for streaming mode.",
            body,
        )


def raise_streaming_error(http_error: MPTHttpError, path: str) -> NoReturn:
    """Re-raise an HTTP error as a typed streaming error when it is a negotiation failure.

    Args:
        http_error: The HTTP error raised while opening the streaming response.
        path: Requested path, used to build the error message.

    Raises:
        MPTStreamingNotSupportedError: If the resource cannot stream (``501``).
        MPTStreamingNotAcceptableError: If the requested format is unsupported (``406``).
        MPTHttpError: Unchanged, for any other status.
    """
    if http_error.status_code == STREAMING_NOT_IMPLEMENTED_STATUS:
        raise MPTStreamingNotSupportedError(path, http_error.body) from http_error
    if http_error.status_code == STREAMING_NOT_ACCEPTABLE_STATUS:
        raise MPTStreamingNotAcceptableError(path, http_error.body) from http_error
    raise http_error


class MPTMaxRetryError(MPTError):
    """Represents an error when maximum retry attempts are exceeded."""

    def __init__(self, message: str, attempts: int):
        super().__init__(f"{message} error after {attempts} retry attempts.")


class MPTAPIError(MPTHttpError):
    """Represents an API error."""

    def __init__(self, status_code: int, message: str, payload: dict[str, str]):
        super().__init__(status_code, message, json.dumps(payload))
        self.payload = payload
        self.status: str | None = payload.get("status") or payload.get("statusCode")
        self.title: str | None = payload.get("title") or payload.get("message")
        self.detail: str | None = payload.get("detail") or message
        self.trace_id: str | None = payload.get("traceId")
        self.errors: str | None = payload.get("errors")

    @override
    def __str__(self) -> str:
        base = f"{self.status} {self.title} - {self.detail} ({self.trace_id or 'no-trace-id'})"  # noqa: WPS221 WPS237

        if self.errors:
            return f"{base}\n{json.dumps(self.errors, indent=2)}"
        return base

    @override
    def __repr__(self) -> str:
        return str(self.payload)


def transform_http_status_exception(http_status_exception: HTTPStatusError) -> MPTError:
    """Transforms httpx exceptions into MPT exceptions.

    Attempts to extract API related information from HTTPStatusError and
    raises MPTAPIError or MPTHttpError.

    Args:
        http_status_exception: Native httpx exception

    Returns:
        MPTError
    """
    try:
        return MPTAPIError(
            status_code=http_status_exception.response.status_code,
            message=http_status_exception.args[0],
            payload=http_status_exception.response.json(),
        )
    except json.JSONDecodeError:
        body = http_status_exception.response.content.decode()
        return MPTHttpError(
            status_code=http_status_exception.response.status_code,
            message=http_status_exception.args[0],
            body=body,
        )
