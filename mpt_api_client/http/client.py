import os
from typing import Any

from httpx import (
    Client,
    HTTPError,
    HTTPStatusError,
    HTTPTransport,
)

from mpt_api_client.exceptions import (
    MPTError,
    transform_http_status_exception,
)
from mpt_api_client.http.types import (
    HeaderTypes,
    QueryParam,
    RequestFiles,
    Response,
)


class HTTPClient:
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
        }
        self.httpx_client = Client(
            base_url=base_url,
            headers=base_headers,
            timeout=timeout,
            transport=HTTPTransport(retries=retries),
        )

    def request(  # noqa: WPS211
        self,
        method: str,
        url: str,
        *,
        files: RequestFiles | None = None,
        json: Any | None = None,
        query_params: QueryParam | None = None,
        headers: HeaderTypes | None = None,
    ) -> Response:
        """Perform an HTTP request.

        Args:
            method: HTTP method.
            url: URL to send the request to.
            files: Request files.
            json: Request JSON data.
            query_params: Query parameters.
            headers: Request headers.

        Returns:
            Response object.

        Raises:
            MPTError: If the request fails.
            MPTApiError: If the response contains an error.
            MPTHttpError: If the response contains an HTTP error.
        """
        try:
            response = self.httpx_client.request(
                method,
                url,
                files=files,
                json=json,
                params=query_params,
                headers=headers,
            )
        except HTTPError as err:
            raise MPTError(f"HTTP Error: {err}") from err

        try:
            response.raise_for_status()
        except HTTPStatusError as http_status_exception:
            raise transform_http_status_exception(http_status_exception) from http_status_exception
        return Response(
            headers=dict(response.headers),
            status_code=response.status_code,
            content=response.content,
        )
