import httpx
import pytest
import respx

from mpt_api_client.resources.notifications.categories import (
    AsyncCategoriesService,
    CategoriesService,
)


@pytest.fixture
def categories_service(http_client):
    return CategoriesService(http_client=http_client)


@pytest.fixture
def async_categories_service(async_http_client):
    return AsyncCategoriesService(http_client=async_http_client)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("publish", {"id": "CAT-123", "status": "to_publish"}),
        ("unpublish", {"id": "CAT-123", "status": "to_unpublish"}),
    ],
)
def test_custom_category_actions(categories_service, action, input_status):
    request_expected_content = b'{"id":"CAT-123","status":"%s"}' % input_status["status"].encode()
    response_expected_data = {"id": "CAT-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/notifications/categories/CAT-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        category = getattr(categories_service, action)("CAT-123", input_status)

        assert mock_route.call_count == 1
        assert category.to_dict() == response_expected_data
        request = mock_route.calls[0].request
        assert request.content == request_expected_content


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("publish", {"id": "CAT-123", "status": "to_publish"}),
        ("unpublish", {"id": "CAT-123", "status": "to_unpublish"}),
    ],
)
async def test_async_custom_category_actions(async_categories_service, action, input_status):
    request_expected_content = b'{"id":"CAT-123","status":"%s"}' % input_status["status"].encode()
    response_expected_data = {"id": "CAT-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/notifications/categories/CAT-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        category = await getattr(async_categories_service, action)("CAT-123", input_status)

        assert category.to_dict() == response_expected_data
        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
