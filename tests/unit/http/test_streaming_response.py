import pytest
from httpx import ConnectTimeout, HTTPError, RemoteProtocolError

from mpt_api_client.exceptions import (
    MPTError,
    MPTMaxRetryError,
    MPTStreamingTruncatedError,
)
from mpt_api_client.http.streaming_response import (
    raise_stream_body_error,
    raise_stream_open_error,
)

STREAM_PATH = "/api/v1/stream"


def test_open_error_is_retry_exhaustion():
    transport_error = ConnectTimeout("Mock Timeout")

    with pytest.raises(MPTMaxRetryError) as raised:
        raise_stream_open_error(transport_error, 4)

    assert str(raised.value) == "Mock Timeout error after 4 retry attempts."
    assert raised.value.__cause__ is transport_error


def test_open_error_other_failure():
    transport_error = HTTPError("Mock protocol failure")

    with pytest.raises(MPTError, match=r"HTTP Error: Mock protocol failure") as raised:
        raise_stream_open_error(transport_error, 4)

    assert not isinstance(raised.value, MPTMaxRetryError)


def test_body_error_is_truncation():
    transport_error = RemoteProtocolError("peer closed connection")

    with pytest.raises(MPTStreamingTruncatedError) as raised:
        raise_stream_body_error(transport_error, STREAM_PATH)

    assert raised.value.path == STREAM_PATH
    assert raised.value.reason == "peer closed connection"
    assert raised.value.__cause__ is transport_error


def test_body_error_other_failure():
    transport_error = HTTPError("Mock protocol failure")

    with pytest.raises(MPTError, match=r"HTTP Error: Mock protocol failure") as raised:
        raise_stream_body_error(transport_error, STREAM_PATH)

    assert not isinstance(raised.value, MPTStreamingTruncatedError)
