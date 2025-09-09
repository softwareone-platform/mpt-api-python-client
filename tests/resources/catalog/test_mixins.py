import httpx
import pytest
import respx

from mpt_api_client.resources.catalog.products import AsyncProductsService, Product, ProductsService


@pytest.fixture
def product_service(http_client):
    return ProductsService(http_client=http_client)


@pytest.fixture
def async_product_service(async_http_client):
    return AsyncProductsService(http_client=async_http_client)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("review", {"id": "PRD-123", "status": "update"}),
        ("publish", {"id": "PRD-123", "status": "update"}),
        ("unpublish", {"id": "PRD-123", "status": "update"}),
    ],
)
def test_custom_resource_actions(product_service, action, input_status):
    request_expected_content = b'{"id":"PRD-123","status":"update"}'
    response_expected_data = {"id": "PRD-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/catalog/products/PRD-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        order = getattr(product_service, action)("PRD-123", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert order.to_dict() == response_expected_data
        assert isinstance(order, Product)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("review", None),
        ("publish", None),
        ("unpublish", None),
    ],
)
def test_custom_resource_actions_no_data(product_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "PRD-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/catalog/products/PRD-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        order = getattr(product_service, action)("PRD-123")

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert order.to_dict() == response_expected_data
        assert isinstance(order, Product)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("review", {"id": "PRD-123", "status": "update"}),
        ("publish", {"id": "PRD-123", "status": "update"}),
        ("unpublish", {"id": "PRD-123", "status": "update"}),
    ],
)
async def test_async_custom_resource_actions(async_product_service, action, input_status):
    request_expected_content = b'{"id":"PRD-123","status":"update"}'
    response_expected_data = {"id": "PRD-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/catalog/products/PRD-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        order = await getattr(async_product_service, action)("PRD-123", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert order.to_dict() == response_expected_data
        assert isinstance(order, Product)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("review", None),
        ("publish", None),
        ("unpublish", None),
    ],
)
async def test_async_custom_resource_actions_no_data(async_product_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "PRD-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/catalog/products/PRD-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        order = await getattr(async_product_service, action)("PRD-123")

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert order.to_dict() == response_expected_data
        assert isinstance(order, Product)
