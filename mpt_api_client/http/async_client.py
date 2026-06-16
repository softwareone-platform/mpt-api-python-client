import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any

from httpx import AsyncClient, HTTPError, RequestError
from httpx import Response as HTTPXResponse
from httpx_retries import Retry, RetryTransport

from mpt_api_client.constants import APPLICATION_JSON
from mpt_api_client.exceptions import MPTError, MPTMaxRetryError
from mpt_api_client.http.client import json_to_file_payload
from mpt_api_client.http.client_utils import get_query_params, validate_base_url
from mpt_api_client.http.query_options import QueryOptions
from mpt_api_client.http.request_response_utils import handle_response_http_error
from mpt_api_client.http.types import HeaderTypes, QueryParam, RequestFiles, Response

if TYPE_CHECKING:
    from mpt_api_client.auth.base import Authentication


class AsyncHTTPClient:
    """Async HTTP client for interacting with SoftwareOne Marketplace Platform API."""

    def __init__(
        self,
        *,
        authentication: "Authentication",
        base_url: str | None = None,
        timeout: float = 20.0,
        retries: int = 5,
    ):
        self._retries = retries
        retry = Retry(
            total=retries,
            allowed_methods={"DELETE", "GET", "HEAD", "OPTIONS", "POST", "PUT", "PATCH"},
        )
        transport = RetryTransport(retry=retry)

        base_url = validate_base_url(base_url or os.getenv("MPT_API_BASE_URL"))
        authentication.configure(base_url=base_url, timeout=timeout, retries=self._retries)
        self.httpx_client = AsyncClient(
            base_url=base_url,
            headers={"User-Agent": "swo-marketplace-client/1.0"},
            auth=authentication,
            timeout=timeout,
            transport=transport,
            follow_redirects=True,
        )

    async def request(  # noqa: WPS211
        self,
        method: str,
        url: str,
        *,
        files: RequestFiles | None = None,
        json: Any | None = None,
        query_params: QueryParam | None = None,
        headers: HeaderTypes | None = None,
        json_file_key: str = "_attachment_data",
        force_multipart: bool = False,
        options: QueryOptions | None = None,
    ) -> Response:
        """Perform an HTTP request.

        Args:
            method: HTTP method.
            url: URL to send the request to.
            files: Request files.
            json: Request JSON data.
            query_params: Query parameters.
            headers: Request headers.
            json_file_key: json file name for data when sending a multipart request.
            force_multipart: force multipart request even if file is not provided.
            options: Additional options for the request.

        Returns:
            Response object.

        Raises:
            MPTError: If the request fails.
            MPTApiError: If the response contains an error.
            MPTHttpError: If the response contains an HTTP error.
            MPTMaxRetryError: If the request fails after maximum retry attempts.
        """
        files = dict(files or {})
        if force_multipart or (files and json):
            files[json_file_key] = (None, json_to_file_payload(json), APPLICATION_JSON)
            json = None
        params_str = get_query_params(query_params, options)
        try:
            response = await self.httpx_client.request(
                method,
                url,
                files=files,
                json=json,
                params=params_str or None,
                headers=headers,
            )
        except RequestError as err:
            raise MPTMaxRetryError(str(err), self._retries + 1) from err
        except HTTPError as err:
            raise MPTError(f"HTTP Error: {err}") from err

        handle_response_http_error(response)

        return Response(
            headers=dict(response.headers),
            status_code=response.status_code,
            content=response.content,
        )

    @asynccontextmanager
    async def stream(
        self,
        method: str,
        url: str,
        *,
        headers: HeaderTypes | None = None,
        query_params: QueryParam | None = None,
        options: QueryOptions | None = None,
    ) -> AsyncIterator[HTTPXResponse]:
        """Open a streaming response without buffering its body fully in memory.

        Useful for JSONL/NDJSON endpoints; callers consume the body via the yielded
        response (e.g. ``aiter_lines()``). Redirects are followed automatically.

        Args:
            method: HTTP method.
            url: URL to send the request to.
            headers: Request headers.
            query_params: Query parameters.
            options: Additional options for the request.

        Yields:
            The open streaming response.

        Raises:
            MPTError: If the request fails.
            MPTApiError: If the response contains an error.
            MPTHttpError: If the response contains an HTTP error.
            MPTMaxRetryError: If the request fails after maximum retry attempts.
        """
        params_str = get_query_params(query_params, options)
        try:
            async with self.httpx_client.stream(
                method, url, params=params_str or None, headers=headers
            ) as response:
                if response.is_error:
                    await response.aread()
                handle_response_http_error(response)
                yield response
        except RequestError as err:
            raise MPTMaxRetryError(str(err), self._retries + 1) from err
        except HTTPError as err:
            raise MPTError(f"HTTP Error: {err}") from err
