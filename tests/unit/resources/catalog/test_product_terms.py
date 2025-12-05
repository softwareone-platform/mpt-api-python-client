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
    result = term_service.path == "/public/v1/catalog/products/PRD-001/terms"

    assert result is True


def test_async_endpoint(async_term_service: AsyncTermService) -> None:
    result = async_term_service.path == "/public/v1/catalog/products/PRD-001/terms"

    assert result is True


@pytest.mark.parametrize(
    "method", ["get", "create", "delete", "update", "review", "publish", "unpublish", "iterate"]
)
def test_methods_present(term_service: TermService, method: str) -> None:
    result = hasattr(term_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method", ["get", "create", "delete", "update", "review", "publish", "unpublish", "iterate"]
)
def test_async_methods_present(async_term_service: AsyncTermService, method: str) -> None:
    result = hasattr(async_term_service, method)

    assert result is True


def test_variants_property(term_service: TermService) -> None:
    result = term_service.variants("TCS-001")

    assert isinstance(result, TermVariantService)
    assert result.http_client == term_service.http_client
    assert result.endpoint_params == {"product_id": "PRD-001", "term_id": "TCS-001"}


def test_async_variants_property(async_term_service: AsyncTermService) -> None:
    result = async_term_service.variants("TCS-001")

    assert isinstance(result, AsyncTermVariantService)
    assert result.http_client == async_term_service.http_client
    assert result.endpoint_params == {"product_id": "PRD-001", "term_id": "TCS-001"}
