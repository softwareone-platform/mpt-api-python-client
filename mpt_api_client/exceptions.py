import json
from typing import override

from httpx import HTTPStatusError


class MPTError(Exception):
    """Represents a generic MPT error."""


class MPTHttpError(MPTError):
    """Represents an HTTP error."""

    def __init__(self, status_code: int, text: str):
        self.status_code = status_code
        self.text = text
        super().__init__(f"{self.status_code} - {self.text}")


class MPTAPIError(MPTHttpError):
    """Represents an API error."""

    def __init__(self, status_code: int, payload: dict[str, str]):
        super().__init__(status_code, json.dumps(payload))
        self.payload = payload
        self.status: str | None = payload.get("status")
        self.title: str | None = payload.get("title")
        self.detail: str | None = payload.get("detail")
        self.trace_id: str | None = payload.get("traceId")
        self.errors: str | None = payload.get("errors")

    @override
    def __str__(self) -> str:
        base = f"{self.status} {self.title} - {self.detail} ({self.trace_id})"

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
            payload=http_status_exception.response.json(),
        )
    except json.JSONDecodeError:
        payload = http_status_exception.response.content.decode()
        return MPTHttpError(
            status_code=http_status_exception.response.status_code,
            text=payload,
        )
