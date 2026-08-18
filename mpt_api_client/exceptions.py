import json
from typing import override

from httpx import HTTPStatusError

from mpt_api_client.constants import MPT_STREAMING_ENABLED, MPT_STREAMING_HEADER


class MPTError(Exception):
    """Represents a generic MPT error."""


class MPTStreamingNotEnabledError(MPTError):
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


class MPTHttpError(MPTError):
    """Represents an HTTP error."""

    def __init__(self, status_code: int, message: str, body: str):
        self.status_code = status_code
        self.body = body
        super().__init__(f"HTTP {status_code}: {message}")


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
