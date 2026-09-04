from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager
from typing import TYPE_CHECKING, Any

from httpx import AsyncClient, HTTPError, RequestError
from httpx import Response as HTTPXResponse
from httpx_retries import RetryTransport

from mpt_api_client.constants import APPLICATION_JSON
from mpt_api_client.exceptions import MPTError, MPTMaxRetryError
from mpt_api_client.http.client import json_to_file_payload
from mpt_api_client.http.client_utils import get_query_params
from mpt_api_client.http.query_options import QueryOptions
from mpt_api_client.http.request_response_utils import handle_response_http_error
from mpt_api_client.http.streaming_response import (
    open_async_stream,
    raise_stream_body_error,
    raise_stream_open_error,
)
from mpt_api_client.http.transport_settings import EnvTransportSettings, TransportSettings
from mpt_api_client.http.types import HeaderTypes, QueryParam, RequestFiles, Response

if TYPE_CHECKING:
    from mpt_api_client.auth.base import Authentication


class AsyncHTTPClient:
    """Async HTTP client for interacting with SoftwareOne Marketplace Platform API."""

    def __init__(
        self,
        transport: TransportSettings | None = None,
        *,
        authentication: "Authentication",
    ):
        """Initialize the client.

        Args:
            transport: Transport settings. Defaults to ``EnvTransportSettings()``,
                which reads the base URL from the ``MPT_API_BASE_URL`` environment
                variable.
            authentication: Authentication provider used for every request.
        """
        self._transport = transport or EnvTransportSettings()
        authentication.configure(self._transport)
        self.httpx_client = AsyncClient(
            base_url=self._transport.url,
            headers={"User-Agent": "swo-marketplace-client/1.0"},
            auth=authentication,
            timeout=self._transport.request_timeout,
            transport=RetryTransport(retry=self._transport.retry),
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
            raise MPTMaxRetryError(str(err), self._transport.retry.total + 1) from err
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

        Prefer the service-level ``stream()`` and ``stream_jsonl()``, which parse the
        records for you; drop to this only for a body they do not model. Redirects are
        followed automatically.

        Split a JSONL/NDJSON body with ``aiter_jsonl_lines(response.aiter_text())`` and
        decode each non-blank line with ``decode_record_line``, both from
        ``mpt_api_client.http.jsonl_lines`` — not with the response's own
        ``aiter_lines()``, which follows ``str.splitlines()`` and so breaks a record at
        U+2028, U+2029 or U+0085, all legal unescaped inside a JSON string value.

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
            MPTMaxRetryError: If opening the response fails after maximum retry attempts.
            MPTStreamingTruncatedError: If the body ends before the HTTP message completes.
        """
        params_str = get_query_params(query_params, options)
        # The guards are split by phase: transparent retry runs while the response is
        # opened, so a failure there is retry exhaustion, while a failure once the body is
        # being consumed can no longer be retried and means the stream was truncated.
        async with AsyncExitStack() as stack:
            stream_context = self.httpx_client.stream(
                method,
                url,
                params=params_str or None,
                headers=headers,
                timeout=self._transport.stream_timeout,
            )
            try:
                response = await open_async_stream(stack, stream_context)
            except HTTPError as open_error:
                raise_stream_open_error(open_error, self._transport.retry.total + 1)
            try:
                yield response
            except HTTPError as body_error:
                raise_stream_body_error(body_error, url)
