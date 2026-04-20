from typing import Any

import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.program.programs_terms import (
    AsyncTermService,
    Term,
    TermService,
)


@pytest.fixture
def term_service(http_client: Any) -> TermService:
    return TermService(http_client=http_client, endpoint_params={"program_id": "PRG-001"})


@pytest.fixture
def async_term_service(async_http_client: Any) -> AsyncTermService:
    return AsyncTermService(
        http_client=async_http_client, endpoint_params={"program_id": "PRG-001"}
    )


@pytest.fixture
def term_data():
    return {
        "id": "PTC-001",
        "name": "Terms of Service",
        "description": "Standard terms",
        "displayOrder": 1,
        "status": "Active",
        "program": {"id": "PRG-001", "name": "My Program"},
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_endpoint(term_service: TermService) -> None:
    result = term_service.path == "/public/v1/program/programs/PRG-001/terms"

    assert result is True


def test_async_endpoint(async_term_service: AsyncTermService) -> None:
    result = async_term_service.path == "/public/v1/program/programs/PRG-001/terms"

    assert result is True


@pytest.mark.parametrize(
    "method", ["get", "create", "delete", "update", "publish", "unpublish", "iterate"]
)
def test_methods_present(term_service: TermService, method: str) -> None:
    result = hasattr(term_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method", ["get", "create", "delete", "update", "publish", "unpublish", "iterate"]
)
def test_async_methods_present(async_term_service: AsyncTermService, method: str) -> None:
    result = hasattr(async_term_service, method)

    assert result is True


def test_term_primitive_fields(term_data: dict) -> None:
    result = Term(term_data)

    assert result.to_dict() == term_data


def test_term_nested_fields_are_base_models(term_data: dict) -> None:
    result = Term(term_data)

    assert isinstance(result.program, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_term_optional_fields_absent() -> None:
    result = Term({"id": "PTC-001"})

    assert result.id == "PTC-001"
    assert not hasattr(result, "name")
    assert not hasattr(result, "description")
    assert not hasattr(result, "display_order")
    assert not hasattr(result, "status")
    assert not hasattr(result, "program")
    assert not hasattr(result, "audit")
