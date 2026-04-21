import pytest
import respx

from mpt_api_client.resources.spotlight.objects import (
    AsyncSpotlightObjectsService,
    SpotlightObjectsService,
)


@pytest.fixture
def spotlight_object_service(http_client):
    return SpotlightObjectsService(http_client=http_client)


@pytest.fixture
def async_spotlight_object_service(async_http_client):
    return AsyncSpotlightObjectsService(http_client=async_http_client)


@pytest.fixture
def spotlight_object_data():
    return {
        "id": "SPO-123",
        "total": 10,
        "top": {"id": "BJO-123", "name": "Top Object"},
        "query": {"id": "SPQ-123", "name": "Spotlight Query"},
    }


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "refresh",
        "iterate",
    ],
)
def test_mixins_present(spotlight_object_service, method):
    result = hasattr(spotlight_object_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "refresh",
        "iterate",
    ],
)
def test_mixins_present_async(async_spotlight_object_service, method):
    result = hasattr(async_spotlight_object_service, method)

    assert result is True


@pytest.mark.parametrize(
    ("object_id", "expected_url"),
    [
        ("SPO-123", "/public/v1/spotlight/objects/SPO-123/refresh"),
        ("-", "/public/v1/spotlight/objects/-/refresh"),
    ],
)
def test_refresh_method(spotlight_object_service, object_id, expected_url):
    with respx.mock(base_url=spotlight_object_service.http_client.httpx_client.base_url) as mock:
        mock.post(expected_url).respond(status_code=204)
        spotlight_object_service.refresh(object_id=object_id)

        result = mock.calls.last.request

        assert result.method == "POST"
        assert result.url.path == expected_url


@pytest.mark.parametrize(
    ("object_id", "expected_url"),
    [
        ("SPO-123", "/public/v1/spotlight/objects/SPO-123/refresh"),
        ("-", "/public/v1/spotlight/objects/-/refresh"),
    ],
)
async def test_refresh_method_async(async_spotlight_object_service, object_id, expected_url):
    with respx.mock(
        base_url=async_spotlight_object_service.http_client.httpx_client.base_url
    ) as mock:
        mock.post(expected_url).respond(status_code=204)
        await async_spotlight_object_service.refresh(object_id=object_id)

        result = mock.calls.last.request

        assert result.method == "POST"
        assert result.url.path == expected_url
