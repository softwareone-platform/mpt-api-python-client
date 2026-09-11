from pathlib import Path

from mpt_api_client.http.types import FileContent, FileTypes

DEFAULT_UPLOAD_FILENAME = "upload"


def _upload_filename(payload: FileContent) -> str:
    """Derive the multipart filename the way httpx does for content passed without one.

    Only a file object opened from a path carries a usable ``name``; ``bytes``, ``str`` and
    ``io.BytesIO`` have none, and a file opened from a descriptor names an ``int``. httpx
    falls back to ``upload`` in each of those cases, so this does too. The basename keeps an
    absolute path out of the multipart part.
    """
    name = getattr(payload, "name", DEFAULT_UPLOAD_FILENAME)

    return Path(str(name)).name or DEFAULT_UPLOAD_FILENAME


def declare_content_type(file_part: FileTypes, content_type: str) -> FileTypes:
    """Declare a content type on a file part unless the caller already declared one.

    httpx derives the content type of an upload from the filename extension and falls back
    to ``application/octet-stream`` whenever :mod:`mimetypes` does not recognise it. The
    API rejects that fallback, so endpoints whose payload extension is unknown to
    :mod:`mimetypes`, such as ``.jsonl``, have to name their own type.

    Args:
        file_part: File part in any of the shapes httpx accepts, which fix the content type
            at the third position: bare content, ``(filename, content)``,
            ``(filename, content, content_type)`` or
            ``(filename, content, content_type, headers)``.
        content_type: Content type to declare when the file part carries none.

    Returns:
        FileTypes: File part with a content type declared.
    """
    if not isinstance(file_part, tuple):
        return _upload_filename(file_part), file_part, content_type

    filename, payload, *type_and_headers = file_part
    declared_type = type_and_headers[0] if type_and_headers else None
    headers = type_and_headers[1:]

    return (filename, payload, declared_type or content_type, *headers)
