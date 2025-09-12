from typing import Any

import pytest

from mpt_api_client.resources.catalog.product_term_variants import (
    AsyncTermVariantService,
    TermVariantService,
)
from mpt_api_client.resources.catalog.product_terms import (
    AsyncTermService,
    TermService,
)


@pytest.fixture
def term_service(http_client: Any) -> TermService:
    return TermService(http_client=http_client, endpoint_params={"product_id": "PRD-001"})


@pytest.fixture
def async_term_service(async_http_client: Any) -> AsyncTermService:
    return AsyncTermService(
        http_client=async_http_client, endpoint_params={"product_id": "PRD-001"}
    )


def test_endpoint(term_service: TermService) -> None:
    assert term_service.endpoint == "/public/v1/catalog/products/PRD-001/terms"


def test_async_endpoint(async_term_service: AsyncTermService) -> None:
    assert async_term_service.endpoint == "/public/v1/catalog/products/PRD-001/terms"


@pytest.mark.parametrize(
    "method", ["get", "create", "delete", "update", "review", "publish", "unpublish"]
)
def test_methods_present(term_service: TermService, method: str) -> None:
    assert hasattr(term_service, method)


@pytest.mark.parametrize(
    "method", ["get", "create", "delete", "update", "review", "publish", "unpublish"]
)
def test_async_methods_present(async_term_service: AsyncTermService, method: str) -> None:
    assert hasattr(async_term_service, method)


def test_variants_property(term_service: TermService) -> None:
    """Test that variants property returns TermVariantService."""
    variants = term_service.variants("TCS-001")
    assert isinstance(variants, TermVariantService)
    assert variants.http_client == term_service.http_client
    assert variants.endpoint_params == {"term_id": "TCS-001"}


def test_async_variants_property(async_term_service: AsyncTermService) -> None:
    """Test that variants property returns AsyncTermVariantService."""
    variants = async_term_service.variants("TCS-001")
    assert isinstance(variants, AsyncTermVariantService)
    assert variants.http_client == async_term_service.http_client
    assert variants.endpoint_params == {"term_id": "TCS-001"}
