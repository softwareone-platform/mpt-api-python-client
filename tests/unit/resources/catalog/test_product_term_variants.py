from typing import Any

import pytest

from mpt_api_client.resources.catalog.product_term_variants import (
    AsyncTermVariantService,
    TermVariantService,
)


@pytest.fixture
def term_variant_service(http_client: Any) -> TermVariantService:
    return TermVariantService(
        http_client=http_client, endpoint_params={"product_id": "PRD-001", "term_id": "TRM-001"}
    )


@pytest.fixture
def async_term_variant_service(async_http_client: Any) -> AsyncTermVariantService:
    return AsyncTermVariantService(
        http_client=async_http_client,
        endpoint_params={"product_id": "PRD-001", "term_id": "TRM-001"},
    )


def test_endpoint(term_variant_service: TermVariantService) -> None:
    result = (
        term_variant_service.path == "/public/v1/catalog/products/PRD-001/terms/TRM-001/variants"
    )

    assert result is True


def test_async_endpoint(async_term_variant_service: AsyncTermVariantService) -> None:
    result = (
        async_term_variant_service.path
        == "/public/v1/catalog/products/PRD-001/terms/TRM-001/variants"
    )

    assert result is True


@pytest.mark.parametrize(
    "method", ["get", "create", "delete", "update", "download", "review", "publish", "unpublish"]
)
def test_methods_present(term_variant_service: TermVariantService, method: str) -> None:
    result = hasattr(term_variant_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method", ["get", "create", "delete", "update", "download", "review", "publish", "unpublish"]
)
def test_async_methods_present(
    async_term_variant_service: AsyncTermVariantService, method: str
) -> None:
    result = hasattr(async_term_variant_service, method)

    assert result is True
