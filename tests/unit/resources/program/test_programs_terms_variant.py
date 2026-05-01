from typing import Any

import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.program.programs_terms_variant import (
    AsyncTermVariantService,
    TermVariant,
    TermVariantService,
)


@pytest.fixture
def term_variant_service(http_client: Any) -> TermVariantService:
    return TermVariantService(
        http_client=http_client, endpoint_params={"program_id": "PRG-001", "term_id": "PTC-001"}
    )


@pytest.fixture
def async_term_variant_service(async_http_client: Any) -> AsyncTermVariantService:
    return AsyncTermVariantService(
        http_client=async_http_client,
        endpoint_params={"program_id": "PRG-001", "term_id": "PTC-001"},
    )


@pytest.fixture
def term_variant_data():
    return {
        "id": "PTV-001",
        "type": "PDF",
        "assetUrl": "https://example.com/file.pdf",
        "languageCode": "en-US",
        "name": "English Terms",
        "description": "English language terms",
        "status": "Active",
        "filename": "terms.pdf",
        "size": 2048,
        "contentType": "application/pdf",
        "programTermsAndConditions": {"id": "PTC-001", "name": "Terms of Service"},
        "fileId": "FILE-001",
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_endpoint(term_variant_service: TermVariantService) -> None:
    result = (
        term_variant_service.path == "/public/v1/program/programs/PRG-001/terms/PTC-001/variants"
    )

    assert result is True


def test_async_endpoint(async_term_variant_service: AsyncTermVariantService) -> None:
    result = (
        async_term_variant_service.path
        == "/public/v1/program/programs/PRG-001/terms/PTC-001/variants"
    )

    assert result is True


@pytest.mark.parametrize(
    "method", ["get", "create", "delete", "update", "publish", "unpublish", "iterate"]
)
def test_methods_present(term_variant_service: TermVariantService, method: str) -> None:
    result = hasattr(term_variant_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method", ["get", "create", "delete", "update", "publish", "unpublish", "iterate"]
)
def test_async_methods_present(
    async_term_variant_service: AsyncTermVariantService, method: str
) -> None:
    result = hasattr(async_term_variant_service, method)

    assert result is True


def test_term_variant_primitive_fields(term_variant_data: dict) -> None:
    result = TermVariant(term_variant_data)

    assert result.to_dict() == term_variant_data


def test_term_variant_inherited_primitive_fields(term_variant_inherited_data: dict) -> None:
    result = TermVariant(term_variant_inherited_data)

    assert result.to_dict() == term_variant_inherited_data


def test_term_variant_nested_base_model(term_variant_data: dict) -> None:
    result = TermVariant(term_variant_data)

    assert isinstance(result.program_terms_and_conditions, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_term_variant_optional_fields_absent() -> None:
    result = TermVariant({"id": "PTV-001"})

    assert result.id == "PTV-001"
    assert result.name is None
    assert result.type is None
    assert result.asset_url is None
    assert result.language_code is None
    assert result.description is None
    assert result.status is None
    assert result.filename is None
    assert result.size is None
    assert result.content_type is None
    assert result.file_id is None
    assert result.program_terms_and_conditions is None
    assert result.audit is None
