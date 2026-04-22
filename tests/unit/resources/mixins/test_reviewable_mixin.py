import httpx
import pytest
import respx

from mpt_api_client.http.async_service import AsyncService
from mpt_api_client.http.service import Service
from mpt_api_client.resources.mixins import (
    AsyncReviewableMixin,
    ReviewableMixin,
)
from tests.unit.conftest import DummyModel


class DummyReviewableService(
    ReviewableMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/reviewable/"
    _model_class = DummyModel
    _collection_key = "data"


class DummyAsyncReviewableService(
    AsyncReviewableMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/reviewable/"
    _model_class = DummyModel
    _collection_key = "data"


@pytest.fixture
def reviewable_service(http_client):
    return DummyReviewableService(http_client=http_client)


@pytest.fixture
def async_reviewable_service(async_http_client):
    return DummyAsyncReviewableService(http_client=async_http_client)


def test_review_with_data(reviewable_service):
    resource_data = {"id": "OBJ-0000-0001", "status": "update"}
    response_expected_data = {"id": "OBJ-0000-0001", "status": "review"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/dummy/reviewable/OBJ-0000-0001/review"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = reviewable_service.review("OBJ-0000-0001", resource_data)

    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.content == b'{"id":"OBJ-0000-0001","status":"update"}'
    assert result.to_dict() == response_expected_data
    assert isinstance(result, DummyModel)


def test_review_no_data(reviewable_service):
    response_expected_data = {"id": "OBJ-0000-0001", "status": "review"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/dummy/reviewable/OBJ-0000-0001/review"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = reviewable_service.review("OBJ-0000-0001")

    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.content == b""
    assert result.to_dict() == response_expected_data
    assert isinstance(result, DummyModel)


async def test_async_review_with_data(async_reviewable_service):
    resource_data = {"id": "OBJ-0000-0001", "status": "update"}
    response_expected_data = {"id": "OBJ-0000-0001", "status": "review"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/dummy/reviewable/OBJ-0000-0001/review"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await async_reviewable_service.review("OBJ-0000-0001", resource_data)

    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.content == b'{"id":"OBJ-0000-0001","status":"update"}'
    assert result.to_dict() == response_expected_data
    assert isinstance(result, DummyModel)


async def test_async_review_no_data(async_reviewable_service):
    response_expected_data = {"id": "OBJ-0000-0001", "status": "review"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/dummy/reviewable/OBJ-0000-0001/review"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await async_reviewable_service.review("OBJ-0000-0001")

    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.content == b""
    assert result.to_dict() == response_expected_data
    assert isinstance(result, DummyModel)
