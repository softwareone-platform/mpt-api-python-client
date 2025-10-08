import os
from typing import Any, override

from httpx import (
    URL,
    USE_CLIENT_DEFAULT,
    Client,
    HTTPError,
    HTTPStatusError,
    HTTPTransport,
    Response,
)
from httpx._client import UseClientDefault
from httpx._types import (
    AuthTypes,
    CookieTypes,
    HeaderTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestExtensions,
    TimeoutTypes,
)
from respx.types import RequestFiles

from mpt_api_client.exceptions import (
    MPTError,
    transform_http_status_exception,
)


class HTTPClient(Client):
    """Sync HTTP client for interacting with SoftwareOne Marketplace Platform API."""

    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_token: str | None = None,
        timeout: float = 5.0,
        retries: int = 5,
    ):
        api_token = api_token or os.getenv("MPT_TOKEN")
        if not api_token:
            raise ValueError(
                "API token is required. "
                "Set it up as env variable MPT_TOKEN or pass it as `api_token` "
                "argument to MPTClient."
            )

        base_url = base_url or os.getenv("MPT_URL")
        if not base_url:
            raise ValueError(
                "Base URL is required. "
                "Set it up as env variable MPT_URL or pass it as `base_url` "
                "argument to MPTClient."
            )
        base_headers = {
            "User-Agent": "swo-marketplace-client/1.0",
            "Authorization": f"Bearer {api_token}",
            "content-type": "application/json",
        }
        super().__init__(
            base_url=base_url,
            headers=base_headers,
            timeout=timeout,
            transport=HTTPTransport(retries=retries),
        )

    @override
    def request(  # noqa: WPS211
        self,
        method: str,
        url: URL | str,
        *,
        content: RequestContent | None = None,  # noqa: WPS110
        data: RequestData | None = None,  # noqa: WPS110
        files: RequestFiles | None = None,
        json: Any | None = None,
        params: QueryParamTypes | None = None,  # noqa: WPS110
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
    ) -> Response:
        try:
            response = super().request(
                method,
                url,
                content=content,
                data=data,
                files=files,
                json=json,
                params=params,
                headers=headers,
                cookies=cookies,
                auth=auth,
            )
        except HTTPError as err:
            raise MPTError(f"HTTP Error: {err}") from err

        try:
            response.raise_for_status()
        except HTTPStatusError as http_status_exception:
            raise transform_http_status_exception(http_status_exception) from http_status_exception
        return response
