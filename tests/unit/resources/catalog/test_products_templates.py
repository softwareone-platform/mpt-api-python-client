import pytest

from mpt_api_client.resources.catalog.products_templates import (
    AsyncTemplatesService,
    TemplatesService,
)


@pytest.fixture
def templates_service(http_client):
    return TemplatesService(http_client=http_client, endpoint_params={"product_id": "PRD-001"})


@pytest.fixture
def async_templates_service(async_http_client):
    return AsyncTemplatesService(
        http_client=async_http_client, endpoint_params={"product_id": "PRD-001"}
    )


def test_endpoint(templates_service):
    result = templates_service.path == "/public/v1/catalog/products/PRD-001/templates"

    assert result is True


def test_async_endpoint(async_templates_service):
    result = async_templates_service.path == "/public/v1/catalog/products/PRD-001/templates"

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "delete", "update", "fetch_page", "iterate"])
def test_methods_present(templates_service, method):
    result = hasattr(templates_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "delete", "update", "fetch_page", "iterate"])
def test_async_methods_present(async_templates_service, method):
    result = hasattr(async_templates_service, method)

    assert result is True
