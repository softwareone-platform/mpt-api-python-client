from httpx import HTTPStatusError
from httpx import Response as HTTPXResponse

from mpt_api_client.exceptions import transform_http_status_exception


def handle_response_http_error(response: HTTPXResponse) -> None:
    """Handles HTTP response error by raising a transformed HTTPStatusError exception."""
    try:
        response.raise_for_status()
    except HTTPStatusError as http_status_exception:
        raise transform_http_status_exception(http_status_exception) from http_status_exception
