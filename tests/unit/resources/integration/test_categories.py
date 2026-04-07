import httpx
import pytest
import respx

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.integration.categories import (
    AsyncCategoriesService,
    CategoriesService,
    Category,
)


@pytest.fixture
def categories_service(http_client):
    return CategoriesService(http_client=http_client)


@pytest.fixture
def async_categories_service(async_http_client):
    return AsyncCategoriesService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "create",
        "update",
        "delete",
        "iterate",
    ],
)
def test_mixins_present(categories_service, method):
    result = hasattr(categories_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "create",
        "update",
        "delete",
        "iterate",
    ],
)
def test_async_mixins_present(async_categories_service, method):
    result = hasattr(async_categories_service, method)

    assert result is True


def test_categories_service_initialization(http_client):
    result = CategoriesService(http_client=http_client)

    assert result.http_client is http_client
    assert isinstance(result, CategoriesService)


def test_async_categories_service_initialization(async_http_client):
    result = AsyncCategoriesService(http_client=async_http_client)

    assert result.http_client is async_http_client
    assert isinstance(result, AsyncCategoriesService)


@pytest.fixture
def category_data():
    return {
        "id": "CAT-001",
        "name": "My Category",
        "revision": 2,
        "description": "A test category",
        "status": "Active",
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_category_primitive_fields(category_data):
    result = Category(category_data)

    assert result.id == "CAT-001"
    assert result.name == "My Category"
    assert result.revision == 2
    assert result.description == "A test category"
    assert result.status == "Active"


def test_category_audit_is_base_model(category_data):
    result = Category(category_data)

    assert isinstance(result.audit, BaseModel)


def test_category_optional_fields_absent():
    result = Category({"id": "CAT-001"})

    assert result.id == "CAT-001"
    assert not hasattr(result, "name")
    assert not hasattr(result, "status")
    assert not hasattr(result, "audit")


def test_category_create(categories_service):
    payload = {"name": "New Category", "description": "Created via API"}
    expected_response = {"id": "CAT-002", "name": "New Category"}
    with respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/integration/categories").mock(
            return_value=httpx.Response(httpx.codes.CREATED, json=expected_response)
        )

        result = categories_service.create(payload)  # act

    assert mock_route.call_count == 1
    assert mock_route.calls[0].request.method == "POST"
    assert result.to_dict() == expected_response


def test_category_list(categories_service):
    response_data = {
        "data": [
            {"id": "CAT-001", "name": "Category One"},
            {"id": "CAT-002", "name": "Category Two"},
        ]
    }
    with respx.mock:
        mock_route = respx.get("https://api.example.com/public/v1/integration/categories").mock(
            return_value=httpx.Response(httpx.codes.OK, json=response_data)
        )

        result = list(categories_service.iterate())  # act

    assert mock_route.call_count == 1
    assert len(result) == 2
    assert result[0].id == "CAT-001"
    assert result[1].id == "CAT-002"
