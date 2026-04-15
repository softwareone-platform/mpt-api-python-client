import re
from typing import Any
from urllib.parse import SplitResult, urlencode, urlsplit, urlunparse

from mpt_api_client.http.query_options import QueryOptions

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


def _append_option(params_str: str, flag: str) -> str:
    return f"{params_str}&{flag}" if params_str else flag


def get_query_params(
    query_params: dict[str, Any] | None, options: QueryOptions | None = None
) -> str:
    """Get query params string from dict."""
    filtered_params = {
        query_param: query_value
        for query_param, query_value in (query_params or {}).items()
        if query_value is not None
    }

    query_params_str = urlencode(filtered_params) if filtered_params else ""

    if options:
        if options.render:
            query_params_str = _append_option(query_params_str, "render()")
        if options.metadata:
            query_params_str = _append_option(query_params_str, "metadata")

    return query_params_str
