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


class DummyService(  # noqa: WPS215
    ManagedResourceMixin[DummyModel],
    CollectionMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/api/v1/test"
    _model_class = DummyModel


class AsyncDummyService(  # noqa: WPS215
    AsyncManagedResourceMixin[DummyModel],
    AsyncCollectionMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/api/v1/test"
    _model_class = DummyModel


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
def filter_status_active():
    return RQLQuery(status="active")
