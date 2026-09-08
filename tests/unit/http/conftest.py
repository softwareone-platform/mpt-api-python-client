import httpx
import pytest

from mpt_api_client import RQLQuery
from mpt_api_client.http import (
    AsyncService,
    Service,
)
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from tests.unit.conftest import DummyModel

# Line-separator characters that are legal unescaped inside a JSON string value, yet
# split a line under str.splitlines() semantics; a JSONL reader must keep them inline.
JSON_LEGAL_SEPARATORS = (
    pytest.param("\u2028", id="U+2028 line separator"),
    pytest.param("\u2029", id="U+2029 paragraph separator"),
    pytest.param("\u0085", id="U+0085 next line"),
)

# Valid JSON that is not a record object: every JSONL reader rejects it with the typed
# decode error instead of failing arbitrarily \u2014 or passing silently \u2014 downstream.
NON_OBJECT_LINE_CASES = (
    pytest.param("42", id="number"),
    pytest.param("null", id="null"),
    pytest.param('"x"', id="string"),
    pytest.param("[1]", id="array"),
)


class DummyService(
    ManagedResourceMixin[DummyModel],
    CollectionMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/api/v1/test"
    _model_class = DummyModel


class AsyncDummyService(
    AsyncManagedResourceMixin[DummyModel],
    AsyncCollectionMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/api/v1/test"
    _model_class = DummyModel


class RecordingProgress:
    """Progress fake recording every event as a tuple, in call order."""

    def __init__(self):
        self.events = []

    def set_total_items(self, total):
        self.events.append(("set_total_items", total))

    def item_processed(self):
        self.events.append(("item_processed",))

    def completed(self):
        self.events.append(("completed",))


class AsyncRecordingProgress:
    """AsyncProgress fake recording every event as a tuple, in call order."""

    def __init__(self):
        self.events = []

    async def set_total_items(self, total):
        self.events.append(("set_total_items", total))

    async def item_processed(self):
        self.events.append(("item_processed",))

    async def completed(self):
        self.events.append(("completed",))


class ClosableByteStream(httpx.SyncByteStream):
    """Response body recording whether the consumer closed it.

    A body backed by bytes reports itself closed from the start, so releasing the
    response is only observable on a stream that records the close itself.
    """

    def __init__(self, body):
        self._body = body
        self.closed = False

    def __iter__(self):
        yield self._body

    def close(self):
        self.closed = True


class ClosableAsyncByteStream(httpx.AsyncByteStream):
    """Async response body recording whether the consumer closed it.

    A body backed by bytes reports itself closed from the start, so releasing the
    response is only observable on a stream that records the close itself.
    """

    def __init__(self, body):
        self._body = body
        self.closed = False

    async def __aiter__(self):
        yield self._body

    async def aclose(self):
        self.closed = True


@pytest.fixture
def recording_progress():
    return RecordingProgress()


@pytest.fixture
def async_recording_progress():
    return AsyncRecordingProgress()


@pytest.fixture
def dummy_service(http_client):
    return DummyService(http_client=http_client)


@pytest.fixture
def async_dummy_service(async_http_client):
    return AsyncDummyService(http_client=async_http_client)


@pytest.fixture
def single_page_response():
    return httpx.Response(
        httpx.codes.OK,
        json={
            "data": [
                {"id": "ID-1", "name": "Resource 1"},
                {"id": "ID-2", "name": "Resource 2"},
            ],
            "$meta": {
                "pagination": {
                    "total": 2,
                    "offset": 0,
                    "limit": 100,
                }
            },
        },
    )


@pytest.fixture
def multi_page_response_page1():
    return httpx.Response(
        httpx.codes.OK,
        json={
            "data": [
                {"id": "ID-1", "name": "Resource 1"},
                {"id": "ID-2", "name": "Resource 2"},
            ],
            "$meta": {
                "pagination": {
                    "total": 4,
                    "offset": 0,
                    "limit": 2,
                }
            },
        },
    )


@pytest.fixture
def multi_page_response_page2():
    return httpx.Response(
        httpx.codes.OK,
        json={
            "data": [
                {"id": "ID-3", "name": "Resource 3"},
                {"id": "ID-4", "name": "Resource 4"},
            ],
            "$meta": {
                "pagination": {
                    "total": 4,
                    "offset": 2,
                    "limit": 2,
                }
            },
        },
    )


@pytest.fixture
def empty_response():
    return httpx.Response(
        httpx.codes.OK,
        json={
            "data": [],
            "$meta": {
                "pagination": {
                    "total": 0,
                    "offset": 0,
                    "limit": 100,
                }
            },
        },
    )


@pytest.fixture
def no_meta_response():
    return httpx.Response(
        httpx.codes.OK,
        json={
            "data": [
                {"id": "ID-1", "name": "Resource 1"},
                {"id": "ID-2", "name": "Resource 2"},
            ]
        },
    )


@pytest.fixture
def list_response():
    return httpx.Response(httpx.codes.OK, json={"data": [{"id": "ID-1"}]})


@pytest.fixture
def single_result_response():
    return httpx.Response(
        httpx.codes.OK,
        json={
            "data": [{"id": "ID-1", "name": "Test Resource"}],
            "$meta": {"pagination": {"total": 1, "offset": 0, "limit": 1}},
        },
    )


@pytest.fixture
def no_results_response():
    return httpx.Response(
        httpx.codes.OK,
        json={"data": [], "$meta": {"pagination": {"total": 0, "offset": 0, "limit": 1}}},
    )


@pytest.fixture
def multiple_results_response():
    return httpx.Response(
        httpx.codes.OK,
        json={
            "data": [{"id": "ID-1", "name": "Resource 1"}, {"id": "ID-2", "name": "Resource 2"}],
            "$meta": {"pagination": {"total": 2, "offset": 0, "limit": 1}},
        },
    )


@pytest.fixture
def deletion_stub_record():
    # Row hard-deleted after the membership snapshot: only "id" is guaranteed on a stub.
    return {"id": "ID-2", "$meta": {"deleted": True}}


@pytest.fixture
def filter_status_active():
    return RQLQuery(status="active")


@pytest.fixture
def mock_httpx_response(mocker):
    response = mocker.Mock(httpx.Response, autospec=True)
    response.headers = {}
    response.status_code = 200
    response.content = ""
    return response
