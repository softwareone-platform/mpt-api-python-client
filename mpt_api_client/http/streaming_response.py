from contextlib import (
    AbstractAsyncContextManager,
    AbstractContextManager,
    AsyncExitStack,
    ExitStack,
)
from typing import NoReturn

from httpx import HTTPError, RequestError
from httpx import Response as HTTPXResponse

from mpt_api_client.exceptions import (
    MPTError,
    MPTMaxRetryError,
    MPTStreamingTruncatedError,
)
from mpt_api_client.http.request_response_utils import handle_response_http_error


def open_stream(
    stack: ExitStack, stream_context: AbstractContextManager[HTTPXResponse]
) -> HTTPXResponse:
    """Open a streaming response and reject it when it carries an error status.

    An error response is read in full first, because its body is the diagnostic and is
    small enough to buffer.

    Args:
        stack: Exit stack that keeps the response open for the caller.
        stream_context: Streaming context that has not been entered yet.

    Returns:
        The open streaming response.
    """
    response = stack.enter_context(stream_context)
    if response.is_error:
        response.read()
    handle_response_http_error(response)
    return response


async def open_async_stream(
    stack: AsyncExitStack, stream_context: AbstractAsyncContextManager[HTTPXResponse]
) -> HTTPXResponse:
    """Open a streaming response and reject it when it carries an error status.

    An error response is read in full first, because its body is the diagnostic and is
    small enough to buffer.

    Args:
        stack: Exit stack that keeps the response open for the caller.
        stream_context: Streaming context that has not been entered yet.

    Returns:
        The open streaming response.
    """
    response = await stack.enter_async_context(stream_context)
    if response.is_error:
        await response.aread()
    handle_response_http_error(response)
    return response


def raise_stream_open_error(transport_error: HTTPError, attempts: int) -> NoReturn:
    """Re-raise a transport failure that happened while the response was being opened.

    The body has not reached the caller yet, so the transparent retry policy has had its
    full budget and a transport failure here means that budget is exhausted.

    Args:
        transport_error: Transport failure raised while opening the response.
        attempts: Number of attempts the retry policy allowed.

    Raises:
        MPTMaxRetryError: If the request never completed after every retry attempt.
        MPTError: For any other transport failure.
    """
    if isinstance(transport_error, RequestError):
        raise MPTMaxRetryError(str(transport_error), attempts) from transport_error
    raise MPTError(f"HTTP Error: {transport_error}") from transport_error


def raise_stream_body_error(transport_error: HTTPError, url: str) -> NoReturn:
    """Re-raise a transport failure that happened while the body was being consumed.

    Transparent retry cannot re-request once the body has started, so a transport failure
    here is a truncated stream rather than retry exhaustion.

    Args:
        transport_error: Transport failure raised while the body was being consumed.
        url: Requested URL, used to build the error message.

    Raises:
        MPTStreamingTruncatedError: If the body ended before the HTTP message completed.
        MPTError: For any other transport failure.
    """
    if isinstance(transport_error, RequestError):
        raise MPTStreamingTruncatedError(url, str(transport_error)) from transport_error
    raise MPTError(f"HTTP Error: {transport_error}") from transport_error
