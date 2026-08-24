import httpx
import pytest
import respx

from mpt_api_client import RQLQuery
from mpt_api_client.exceptions import (
    MPTHttpError,
    MPTStreamingError,
    MPTStreamingIncompleteError,
    MPTStreamingItemCountMissingError,
    MPTStreamingNotAcceptableError,
    MPTStreamingNotEnabledError,
    MPTStreamingNotSupportedError,
    MPTStreamingOverCapError,
)
from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import AsyncStreamingMixin, StreamingMixin
from mpt_api_client.http.mixins.streaming_mixin import declared_item_count
from tests.unit.conftest import API_URL, DummyModel
from tests.unit.http.conftest import AsyncRecordingProgress, RecordingProgress

STREAM_URL = f"{API_URL}/api/v1/orders"
JSONL_BODY = b'{"id": "ID-1", "name": "Order 1"}\n\n{"id": "ID-2", "name": "Order 2"}\n'
NOT_CONFIRMED_MATCH = "did not confirm streaming mode"
COUNT_MISSING_MATCH = "did not declare the item count"
COUNT_MISMATCH_MATCH = "declared 3, received 2"
BOUNDED_LIMIT = 100
PASSED_OFFSET = 50
BOUNDED_QUERY = "limit=100&offset=50"

# Pagination inputs reach the server exactly as given, and an unset input is omitted rather
# than defaulted. Nothing here is validated locally: the server owns pagination-input
# validation, and offset is scheduled for support there, so a client-side guard would expire.
PAGINATION_CASES = (
    pytest.param({}, "", id="unset - absent limit is the full snapshot"),
    pytest.param({"limit": -1}, "limit=-1", id="-1 - the same thing, said explicitly"),
    pytest.param({"limit": 0}, "limit=0", id="zero - passed through, not corrected"),
    pytest.param({"limit": BOUNDED_LIMIT}, "limit=100", id="bounded prefix of the t0 order"),
    pytest.param({"offset": 0}, "offset=0", id="offset zero is still sent"),
    pytest.param({"offset": PASSED_OFFSET}, "offset=50", id="offset - the server decides"),
    pytest.param(
        {"limit": BOUNDED_LIMIT, "offset": PASSED_OFFSET}, BOUNDED_QUERY, id="both together"
    ),
)

# Every unusable MPT-Item-Count value takes the same failure path before the body is read.
UNUSABLE_COUNT_CASES = (
    pytest.param({"MPT-Streaming": "true"}, id="absent"),
    pytest.param({"MPT-Streaming": "true", "MPT-Item-Count": "-1"}, id="negative"),
    pytest.param({"MPT-Streaming": "true", "MPT-Item-Count": "abc"}, id="not a number"),
    pytest.param({"MPT-Streaming": "true", "MPT-Item-Count": ""}, id="empty"),
)


class DummyStreamingService(
    StreamingMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/api/v1/orders"
    _model_class = DummyModel


class AsyncDummyStreamingService(
    AsyncStreamingMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/api/v1/orders"
    _model_class = DummyModel


@pytest.fixture
def streaming_service(http_client):
    return DummyStreamingService(http_client=http_client)


@pytest.fixture
def async_streaming_service(async_http_client):
    return AsyncDummyStreamingService(http_client=async_http_client)


def streaming_response(item_count="2"):
    return jsonl_response({"MPT-Streaming": "true", "MPT-Item-Count": item_count})


def jsonl_response(headers=None):
    return httpx.Response(httpx.codes.OK, content=JSONL_BODY, headers=headers)


@respx.mock
def test_stream_sends_streaming_opt_in_headers(streaming_service):
    route = respx.get(STREAM_URL).mock(return_value=streaming_response())

    list(streaming_service.stream())  # act

    request = route.calls[0].request
    assert request.headers["MPT-Streaming"] == "true"
    assert request.headers["Accept"] == "application/jsonl"


@pytest.mark.parametrize(
    "pagination",
    [
        pytest.param({}, id="full snapshot"),
        pytest.param({"limit": BOUNDED_LIMIT}, id="bounded export"),
    ],
)
@respx.mock
def test_stream_yields_models(streaming_service, pagination):
    respx.get(STREAM_URL).mock(return_value=streaming_response())

    result = list(streaming_service.stream(**pagination))

    assert [order.id for order in result] == ["ID-1", "ID-2"]
    assert all(isinstance(order, DummyModel) for order in result)


@respx.mock
def test_stream_applies_query_filters(streaming_service):
    route = respx.get(STREAM_URL).mock(return_value=streaming_response())

    result = list(streaming_service.filter(RQLQuery(status="active")).stream())

    request = route.calls[0].request
    assert result
    assert "status" in request.url.query.decode()


@pytest.mark.parametrize(("pagination", "expected_query"), PAGINATION_CASES)
@respx.mock
def test_stream_sends_pagination_params(streaming_service, pagination, expected_query):
    route = respx.get(STREAM_URL).mock(return_value=streaming_response())

    list(streaming_service.stream(**pagination))  # act

    request = route.calls[0].request
    assert request.url.query.decode() == expected_query


@respx.mock
def test_stream_combines_limit_with_query_state(streaming_service):
    route = respx.get(STREAM_URL).mock(return_value=streaming_response())
    bounded_service = streaming_service.filter(RQLQuery(status="active")).select("id")

    list(bounded_service.stream(limit=BOUNDED_LIMIT))  # act

    request = route.calls[0].request
    assert request.url.query.decode() == "limit=100&select=id&eq(status,'active')"


@pytest.mark.parametrize(
    ("headers", "error_match"),
    [
        pytest.param(None, NOT_CONFIRMED_MATCH, id="header absent"),
        pytest.param({"MPT-Streaming": "false"}, "got 'false'", id="explicit false"),
    ],
)
@respx.mock
def test_stream_raises_when_not_confirmed(streaming_service, headers, error_match):
    respx.get(STREAM_URL).mock(return_value=jsonl_response(headers))
    iterator = streaming_service.stream()

    with pytest.raises(MPTStreamingNotEnabledError, match=error_match):
        next(iterator)


@respx.mock
def test_stream_accepts_uppercase_value(streaming_service):
    respx.get(STREAM_URL).mock(
        return_value=jsonl_response({"MPT-Streaming": "True", "MPT-Item-Count": "2"})
    )

    result = list(streaming_service.stream())

    assert [order.id for order in result] == ["ID-1", "ID-2"]


@respx.mock
def test_stream_progress_events(streaming_service, recording_progress: RecordingProgress):
    respx.get(STREAM_URL).mock(return_value=streaming_response())

    list(streaming_service.stream(progress=recording_progress))  # act

    assert recording_progress.events == [
        ("item_processed",),
        ("item_processed",),
        ("completed",),
    ]


@respx.mock
async def test_async_stream_sends_opt_in_headers(async_streaming_service):
    route = respx.get(STREAM_URL).mock(return_value=streaming_response())

    [order async for order in async_streaming_service.stream()]  # act

    request = route.calls[0].request
    assert request.headers["MPT-Streaming"] == "true"
    assert request.headers["Accept"] == "application/jsonl"


@respx.mock
async def test_async_stream_yields_models(async_streaming_service):
    respx.get(STREAM_URL).mock(return_value=streaming_response())

    result = [order async for order in async_streaming_service.stream()]

    assert [order.id for order in result] == ["ID-1", "ID-2"]
    assert all(isinstance(order, DummyModel) for order in result)


@pytest.mark.parametrize(("pagination", "expected_query"), PAGINATION_CASES)
@respx.mock
async def test_async_stream_sends_pagination_params(
    async_streaming_service, pagination, expected_query
):
    route = respx.get(STREAM_URL).mock(return_value=streaming_response())
    stream = async_streaming_service.stream(**pagination)

    [order async for order in stream]  # act

    request = route.calls[0].request
    assert request.url.query.decode() == expected_query


@respx.mock
async def test_async_stream_raises_not_confirmed(async_streaming_service):
    respx.get(STREAM_URL).mock(return_value=jsonl_response())
    iterator = async_streaming_service.stream()

    with pytest.raises(MPTStreamingNotEnabledError, match=NOT_CONFIRMED_MATCH):
        await anext(iterator)


@respx.mock
async def test_async_stream_progress_events(
    async_streaming_service, async_recording_progress: AsyncRecordingProgress
):
    respx.get(STREAM_URL).mock(return_value=streaming_response())

    [order async for order in async_streaming_service.stream(progress=async_recording_progress)]

    assert async_recording_progress.events == [
        ("item_processed",),
        ("item_processed",),
        ("completed",),
    ]


@pytest.mark.parametrize(
    ("status_code", "error_class", "error_match"),
    [
        pytest.param(
            httpx.codes.NOT_IMPLEMENTED,
            MPTStreamingNotSupportedError,
            "does not support streaming mode",
            id="501 not supported",
        ),
        pytest.param(
            httpx.codes.NOT_ACCEPTABLE,
            MPTStreamingNotAcceptableError,
            "requested streaming format",
            id="406 not acceptable",
        ),
    ],
)
@respx.mock
def test_stream_raises_typed_negotiation_error(
    streaming_service, status_code, error_class, error_match
):
    respx.get(STREAM_URL).mock(return_value=httpx.Response(status_code))
    iterator = streaming_service.stream()

    with pytest.raises(error_class, match=error_match):
        next(iterator)


@respx.mock
def test_streaming_errors_stay_catchable_as_http(streaming_service):
    respx.get(STREAM_URL).mock(return_value=httpx.Response(httpx.codes.NOT_IMPLEMENTED))
    iterator = streaming_service.stream()

    with pytest.raises(MPTHttpError) as raised:
        next(iterator)

    assert raised.value.status_code == httpx.codes.NOT_IMPLEMENTED
    assert isinstance(raised.value, MPTStreamingError)


@pytest.mark.parametrize(
    ("pagination", "status_code"),
    [
        pytest.param({"offset": PASSED_OFFSET}, httpx.codes.BAD_REQUEST, id="offset rejection"),
        pytest.param({}, httpx.codes.FORBIDDEN, id="unrelated failure"),
    ],
)
@respx.mock
def test_other_http_errors_are_not_translated(streaming_service, pagination, status_code):
    respx.get(STREAM_URL).mock(return_value=httpx.Response(status_code))
    iterator = streaming_service.stream(**pagination)

    with pytest.raises(MPTHttpError) as raised:
        next(iterator)

    assert raised.value.status_code == status_code
    assert not isinstance(raised.value, MPTStreamingError)


@pytest.mark.parametrize(
    "headers",
    [
        pytest.param(None, id="not enabled"),
        pytest.param({"MPT-Streaming": "true", "MPT-Item-Count": "3"}, id="incomplete"),
    ],
)
@respx.mock
def test_errors_are_streaming_errors(streaming_service, headers):
    respx.get(STREAM_URL).mock(return_value=jsonl_response(headers))
    iterator = streaming_service.stream()

    with pytest.raises(MPTStreamingError):
        list(iterator)


@pytest.mark.parametrize(
    ("status_code", "error_class"),
    [
        pytest.param(httpx.codes.NOT_IMPLEMENTED, MPTStreamingNotSupportedError, id="501"),
        pytest.param(httpx.codes.NOT_ACCEPTABLE, MPTStreamingNotAcceptableError, id="406"),
    ],
)
@respx.mock
async def test_async_stream_raises_negotiation_error(
    async_streaming_service, status_code, error_class
):
    respx.get(STREAM_URL).mock(return_value=httpx.Response(status_code))
    iterator = async_streaming_service.stream()

    with pytest.raises(error_class):
        await anext(iterator)


def test_declared_item_count_reads_header():
    headers = {"MPT-Item-Count": "0"}

    result = declared_item_count(headers, "/api/v1/orders")

    assert result == 0


@pytest.mark.parametrize(
    ("item_count", "mismatch_match"),
    [
        pytest.param("3", COUNT_MISMATCH_MATCH, id="short stream"),
        pytest.param("1", "declared 1, received 2", id="extra records"),
    ],
)
@respx.mock
def test_stream_raises_on_count_mismatch(streaming_service, item_count, mismatch_match):
    respx.get(STREAM_URL).mock(return_value=streaming_response(item_count=item_count))
    iterator = streaming_service.stream()

    with pytest.raises(MPTStreamingIncompleteError, match=mismatch_match):
        list(iterator)


@respx.mock
def test_stream_incomplete_error_counts(streaming_service):
    respx.get(STREAM_URL).mock(return_value=streaming_response(item_count="3"))
    iterator = streaming_service.stream()

    with pytest.raises(MPTStreamingIncompleteError) as raised:
        list(iterator)

    assert (raised.value.expected_count, raised.value.received_count) == (3, 2)


@pytest.mark.parametrize("headers", UNUSABLE_COUNT_CASES)
@respx.mock
def test_stream_raises_on_unusable_item_count(streaming_service, headers):
    respx.get(STREAM_URL).mock(return_value=jsonl_response(headers))
    iterator = streaming_service.stream()

    with pytest.raises(MPTStreamingItemCountMissingError, match=COUNT_MISSING_MATCH):
        next(iterator)


@respx.mock
def test_stream_early_close_skips_verification(streaming_service):
    respx.get(STREAM_URL).mock(return_value=streaming_response(item_count="3"))
    iterator = streaming_service.stream()
    first = next(iterator)

    iterator.close()  # act

    assert first.id == "ID-1"


@respx.mock
def test_incomplete_skips_progress_completed(streaming_service, recording_progress):
    respx.get(STREAM_URL).mock(return_value=streaming_response(item_count="3"))
    iterator = streaming_service.stream(progress=recording_progress)

    with pytest.raises(MPTStreamingIncompleteError):
        list(iterator)

    assert recording_progress.events == [("item_processed",), ("item_processed",)]


@respx.mock
async def test_async_stream_raises_when_stream_is_short(async_streaming_service):
    respx.get(STREAM_URL).mock(return_value=streaming_response(item_count="3"))
    iterator = async_streaming_service.stream()

    with pytest.raises(MPTStreamingIncompleteError, match=COUNT_MISMATCH_MATCH):
        [order async for order in iterator]


@pytest.mark.parametrize("headers", UNUSABLE_COUNT_CASES)
@respx.mock
async def test_async_stream_raises_on_unusable_count(async_streaming_service, headers):
    respx.get(STREAM_URL).mock(return_value=jsonl_response(headers))
    iterator = async_streaming_service.stream()

    with pytest.raises(MPTStreamingItemCountMissingError, match=COUNT_MISSING_MATCH):
        await anext(iterator)


@respx.mock
async def test_async_early_close_skips_verification(async_streaming_service):
    respx.get(STREAM_URL).mock(return_value=streaming_response(item_count="3"))
    iterator = async_streaming_service.stream()
    first = await anext(iterator)

    await iterator.aclose()  # act

    assert first.id == "ID-1"


def over_cap_problem():
    return {
        "type": "https://api.s1.show/problems/export-too-large",
        "title": "Export too large",
        "status": 413,
        "detail": "the result set exceeds the configured MaxExportKeys of 500000",
        "maxExportKeys": 500000,
    }


def over_cap_response():
    return httpx.Response(
        httpx.codes.REQUEST_ENTITY_TOO_LARGE,
        json=over_cap_problem(),
        headers={"Content-Type": "application/problem+json"},
    )


@respx.mock
def test_stream_raises_when_over_cap(streaming_service):
    respx.get(STREAM_URL).mock(return_value=over_cap_response())
    iterator = streaming_service.stream()

    with pytest.raises(MPTStreamingOverCapError) as raised:
        next(iterator)

    assert raised.value.payload == over_cap_problem()
    assert raised.value.status_code == httpx.codes.REQUEST_ENTITY_TOO_LARGE


@respx.mock
async def test_async_stream_raises_when_over_cap(async_streaming_service):
    respx.get(STREAM_URL).mock(return_value=over_cap_response())
    iterator = async_streaming_service.stream()

    with pytest.raises(MPTStreamingOverCapError) as raised:
        await anext(iterator)

    assert raised.value.payload == over_cap_problem()
