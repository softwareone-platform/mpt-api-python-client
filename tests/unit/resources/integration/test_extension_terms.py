from typing import Any

import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.integration.extension_term_variants import (
    AsyncExtensionTermVariantsService,
    ExtensionTermVariantsService,
)
from mpt_api_client.resources.integration.extension_terms import (
    AsyncExtensionTermsService,
    ExtensionTerm,
    ExtensionTermsService,
)
from mpt_api_client.resources.integration.extensions import (
    AsyncExtensionsService,
    ExtensionsService,
)


@pytest.fixture
def terms_service(http_client: Any) -> ExtensionTermsService:
    return ExtensionTermsService(
        http_client=http_client, endpoint_params={"extension_id": "EXT-001"}
    )


@pytest.fixture
def async_terms_service(async_http_client: Any) -> AsyncExtensionTermsService:
    return AsyncExtensionTermsService(
        http_client=async_http_client, endpoint_params={"extension_id": "EXT-001"}
    )


@pytest.fixture
def extensions_service(http_client: Any) -> ExtensionsService:
    return ExtensionsService(http_client=http_client)


@pytest.fixture
def async_extensions_service(async_http_client: Any) -> AsyncExtensionsService:
    return AsyncExtensionsService(http_client=async_http_client)


@pytest.fixture
def term_data():
    return {
        "id": "TERM-001",
        "name": "Acceptable Use Policy",
        "revision": 1,
        "description": "Standard acceptable use policy",
        "displayOrder": 1,
        "status": "Draft",
        "extension": {"id": "EXT-001"},
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


@pytest.mark.parametrize(
    "method", ["get", "create", "update", "delete", "publish", "unpublish", "iterate"]
)
def test_mixins_present(terms_service: ExtensionTermsService, method: str) -> None:
    result = hasattr(terms_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method", ["get", "create", "update", "delete", "publish", "unpublish", "iterate"]
)
def test_async_mixins_present(async_terms_service: AsyncExtensionTermsService, method: str) -> None:
    result = hasattr(async_terms_service, method)

    assert result is True


def test_extension_term_primitive_fields(term_data: dict) -> None:
    result = ExtensionTerm(term_data)

    assert result.to_dict() == term_data


def test_extension_term_nested_fields(term_data: dict) -> None:
    result = ExtensionTerm(term_data)

    assert isinstance(result.extension, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_extension_term_create(terms_service: ExtensionTermsService) -> None:
    result = hasattr(terms_service, "create")

    assert result is True


def test_extension_terms_variants_accessor(terms_service: ExtensionTermsService) -> None:
    result = terms_service.variants("TERM-001")

    assert isinstance(result, ExtensionTermVariantsService)
    assert result.http_client == terms_service.http_client
    assert result.endpoint_params == {"extension_id": "EXT-001", "term_id": "TERM-001"}


def test_async_extension_terms_variants_accessor(
    async_terms_service: AsyncExtensionTermsService,
) -> None:
    result = async_terms_service.variants("TERM-001")

    assert isinstance(result, AsyncExtensionTermVariantsService)
    assert result.http_client == async_terms_service.http_client
    assert result.endpoint_params == {"extension_id": "EXT-001", "term_id": "TERM-001"}


def test_extensions_terms_accessor(extensions_service: ExtensionsService) -> None:
    result = extensions_service.terms("EXT-001")

    assert isinstance(result, ExtensionTermsService)
    assert result.http_client == extensions_service.http_client
    assert result.endpoint_params == {"extension_id": "EXT-001"}


def test_async_extensions_terms_accessor(
    async_extensions_service: AsyncExtensionsService,
) -> None:
    result = async_extensions_service.terms("EXT-001")

    assert isinstance(result, AsyncExtensionTermsService)
    assert result.http_client == async_extensions_service.http_client
    assert result.endpoint_params == {"extension_id": "EXT-001"}
