from typing import Any

import httpx
import pytest
import respx

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.integration.extension_term_variants import (
    AsyncExtensionTermVariantsService,
    ExtensionTermVariant,
    ExtensionTermVariantsService,
)
from mpt_api_client.resources.integration.extension_terms import ExtensionTermsService

BASE_URL = "https://api.example.com"
VARIANTS_URL = f"{BASE_URL}/public/v1/integration/extensions/EXT-001/terms/TERM-001/variants"


@pytest.fixture
def variants_service(http_client: Any) -> ExtensionTermVariantsService:
    return ExtensionTermVariantsService(
        http_client=http_client,
        endpoint_params={"extension_id": "EXT-001", "term_id": "TERM-001"},
    )


@pytest.fixture
def async_variants_service(async_http_client: Any) -> AsyncExtensionTermVariantsService:
    return AsyncExtensionTermVariantsService(
        http_client=async_http_client,
        endpoint_params={"extension_id": "EXT-001", "term_id": "TERM-001"},
    )


@pytest.fixture
def terms_service(http_client: Any) -> ExtensionTermsService:
    return ExtensionTermsService(
        http_client=http_client, endpoint_params={"extension_id": "EXT-001"}
    )


@pytest.fixture
def variant_data() -> dict:
    return {
        "id": "TRV-001",
        "name": "English Variant",
        "revision": 1,
        "type": "File",
        "assetUrl": None,
        "languageCode": "en-US",
        "description": "English language variant",
        "status": "Draft",
        "filename": "terms.pdf",
        "size": 2048,
        "contentType": "application/pdf",
        "term": {"id": "TERM-001"},
        "fileId": "FILE-001",
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "publish", "unpublish", "iterate"],
)
def test_mixins_present(variants_service: ExtensionTermVariantsService, method: str) -> None:
    result = hasattr(variants_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "publish", "unpublish", "iterate"],
)
def test_async_mixins_present(
    async_variants_service: AsyncExtensionTermVariantsService, method: str
) -> None:
    result = hasattr(async_variants_service, method)

    assert result is True


def test_extension_term_variant_primitive_fields(variant_data: dict) -> None:
    result = ExtensionTermVariant(variant_data)

    assert result.to_dict() == variant_data


def test_extension_term_variant_nested_fields(variant_data: dict) -> None:
    result = ExtensionTermVariant(variant_data)

    assert isinstance(result.term, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_extension_term_variant_create(
    variants_service: ExtensionTermVariantsService, tmp_path: Any
) -> None:
    variant_payload = {
        "Type": "File",
        "Name": "English Variant",
        "LanguageCode": "en-US",
        "Description": "English language variant",
    }
    response_data = {"id": "TRV-001", "name": "English Variant", "status": "Draft"}
    with respx.mock:
        mock_route = respx.post(VARIANTS_URL).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_data,
            )
        )
        file_path = tmp_path / "terms.pdf"
        file_path.write_bytes(b"fake-pdf-content")

        with file_path.open("rb") as fp:
            result = variants_service.create(variant_payload, fp)

    assert mock_route.call_count == 1
    assert result.to_dict() == response_data


def test_extension_term_variant_get(
    variants_service: ExtensionTermVariantsService, variant_data: dict
) -> None:
    with respx.mock:
        respx.get(f"{VARIANTS_URL}/TRV-001").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=variant_data,
            )
        )

        result = variants_service.get("TRV-001")

    assert result.to_dict() == variant_data


def test_extension_term_variants_list(
    variants_service: ExtensionTermVariantsService, variant_data: dict
) -> None:
    response_data = {
        "data": [variant_data],
        "$meta": {"pagination": {"total": 1, "offset": 0, "limit": 100}},
    }
    with respx.mock:
        respx.get(VARIANTS_URL).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=response_data,
            )
        )

        result = variants_service.fetch_page()

    assert result[0].to_dict() == variant_data


def test_extension_term_variants_service_endpoint(
    variants_service: ExtensionTermVariantsService,
) -> None:
    result = variants_service.path

    assert result == "/public/v1/integration/extensions/EXT-001/terms/TERM-001/variants"


def test_extension_terms_variants_accessor(terms_service: ExtensionTermsService) -> None:
    result = terms_service.variants("TERM-001")

    assert isinstance(result, ExtensionTermVariantsService)
    assert result.http_client == terms_service.http_client
    assert result.endpoint_params == {"extension_id": "EXT-001", "term_id": "TERM-001"}
