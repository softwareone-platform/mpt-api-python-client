import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.billing.statement_charges import (
    AsyncStatementChargesService,
    StatementCharge,
    StatementChargesService,
)


@pytest.fixture
def statement_charges_service(http_client):
    return StatementChargesService(
        http_client=http_client, endpoint_params={"statement_id": "STM-0000-0001"}
    )


@pytest.fixture
def async_statement_charges_service(async_http_client):
    return AsyncStatementChargesService(
        http_client=async_http_client, endpoint_params={"statement_id": "STM-0000-0001"}
    )


def test_endpoint(statement_charges_service):
    result = statement_charges_service.path == (
        "/public/v1/billing/statements/STM-0000-0001/charges"
    )

    assert result is True


def test_async_endpoint(async_statement_charges_service):
    result = async_statement_charges_service.path == (
        "/public/v1/billing/statements/STM-0000-0001/charges"
    )

    assert result is True


@pytest.mark.parametrize("method", ["get", "stream"])
def test_methods_present(statement_charges_service, method):
    result = hasattr(statement_charges_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "stream"])
def test_async_methods_present(async_statement_charges_service, method):
    result = hasattr(async_statement_charges_service, method)

    assert result is True


@pytest.fixture
def charge_data():
    return {
        "id": "CHG-0001",
        "revision": 3,
        "quantity": 10.5,
        "billingType": "automated",
        "statementType": "Standard",
        "externalIds": {"invoice": "INV12345"},
        "price": {"unitPP": 10, "PPx1": 8.33},
        "period": {"start": "2025-01-01", "end": "2025-12-31"},
        "description": {"value1": "desc-1"},
        "statement": {"id": "STM-0000-0001"},
        "journal": {"id": "BJO-0001"},
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_charge_primitive_fields(charge_data):
    result = StatementCharge(charge_data)

    assert result.to_dict() == charge_data


def test_charge_typed_scalar_fields(charge_data):  # noqa: WPS218
    result = StatementCharge(charge_data)

    assert result.id == "CHG-0001"
    assert result.revision == 3
    assert result.quantity == pytest.approx(10.5)
    assert result.billing_type == "automated"
    assert result.statement_type == "Standard"


def test_charge_nested_fields(charge_data):  # noqa: WPS218
    result = StatementCharge(charge_data)

    assert isinstance(result.external_ids, BaseModel)
    assert isinstance(result.price, BaseModel)
    assert isinstance(result.period, BaseModel)
    assert isinstance(result.statement, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_charge_optional_fields_absent():
    result = StatementCharge({"id": "CHG-0001"})

    assert result.id == "CHG-0001"
    assert not hasattr(result, "price")
    assert not hasattr(result, "external_ids")
