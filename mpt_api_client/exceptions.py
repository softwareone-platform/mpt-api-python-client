import json
from typing import override

from httpx import HTTPStatusError


class MPTError(Exception):
    """Represents a generic MPT error."""


class MPTHttpError(MPTError):
    """Represents an HTTP error."""

    def __init__(self, status_code: int, message: str, body: str):
        self.status_code = status_code
        self.body = body
        super().__init__(f"HTTP {status_code}: {message}")


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
