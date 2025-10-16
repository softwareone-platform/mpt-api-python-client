import json
from collections.abc import Mapping, Sequence
from typing import IO, Any

PrimitiveType = str | int | float | bool | None
QueryParam = dict[str, PrimitiveType]
HeaderTypes = dict[str, str]

# Borrowed from HTTPX's "private" types.
FileContent = IO[bytes] | bytes | str
FileTypes = (
    # file (or bytes)
    FileContent
    |
    # (filename, file (or bytes))
    tuple[str | None, FileContent]
    |
    # (filename, file (or bytes), content_type)
    tuple[str | None, FileContent, str | None]
    |
    # (filename, file (or bytes), content_type, headers)
    tuple[str | None, FileContent, str | None, Mapping[str, str]]  # noqa: WPS221
)
RequestFiles = Mapping[str, FileTypes] | Sequence[tuple[str, FileTypes]]  # noqa: WPS221


class Response:
    """HTTP Response."""

    def __init__(self, headers: HeaderTypes, status_code: int, content: bytes):  # noqa: WPS110
        self.headers = headers
        self.status_code = status_code
        self.content = content  # noqa: WPS110

    @property
    def text(self) -> str:
        """Content of the response, as text."""
        return self.content.decode()

    def json(self, **kwargs: Any) -> Any:
        """Return the json-encoded content of a response, if any."""
        return json.loads(self.content, **kwargs)
