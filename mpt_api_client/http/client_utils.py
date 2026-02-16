import re
from urllib.parse import SplitResult, urlsplit, urlunparse

INVALID_ENV_URL_MESSAGE = (
    "Base URL is required. "
    "Set it up as env variable MPT_URL or pass it as `base_url` "
    "argument to MPTClient. Expected format scheme://host[:port]"
)
PATHS_TO_REMOVE_RE = re.compile(r"^/$|^/public/?$|^/public/v1/?$")


def _format_host(hostname: str | None) -> str:
    if not hostname or not isinstance(hostname, str):
        raise ValueError(INVALID_ENV_URL_MESSAGE)

    return f"[{hostname}]" if ":" in hostname else hostname


def _format_port(split_result: SplitResult) -> str:
    try:
        parsed_port = split_result.port
    except ValueError as exc:
        raise ValueError(INVALID_ENV_URL_MESSAGE) from exc
    return f":{parsed_port}" if parsed_port else ""


def _sanitize_path(path: str) -> str:
    return PATHS_TO_REMOVE_RE.sub("", path)


def _build_sanitized_base_url(split_result: SplitResult) -> str:
    host = _format_host(split_result.hostname)
    port = _format_port(split_result)
    path = _sanitize_path(split_result.path)
    return str(urlunparse((split_result.scheme, f"{host}{port}", path, "", "", "")))


def validate_base_url(base_url: str | None) -> str:
    """Validate base url."""
    if not base_url or not isinstance(base_url, str):
        raise ValueError(INVALID_ENV_URL_MESSAGE)

    split_result = urlsplit(base_url, scheme="https")
    if not split_result.scheme or not split_result.hostname:
        raise ValueError(INVALID_ENV_URL_MESSAGE)

    return _build_sanitized_base_url(split_result)
