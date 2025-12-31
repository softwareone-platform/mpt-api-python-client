import pytest
from freezegun import freeze_time


@pytest.fixture
def custom_ledger_id(e2e_config):
    return e2e_config["billing.custom_ledger.id"]


@pytest.fixture
def invalid_custom_ledger_id():
    return "CLD-0000-0000"


@pytest.fixture
@freeze_time("2025-12-01T10:00:00.000Z")
def custom_ledger_factory(
    account_seller_id,
    account_id,
):
    def factory(
        notes: str = "E2E Created Custom Ledger",
    ):
        return {
            "seller": {"id": account_seller_id},
            "vendor": {"id": account_id},
            "price": {
                "markup": 10,
                "margin": 10,
                "totalPP": 100,
                "totalSP": 100,
                "currency": {
                    "purchase": "USD",
                    "sale": "USD",
                    "rate": 1,
                },
                "assignee": {},
            },
            "notes": notes,
            "status": "Validated",
            "billingStartDate": "2025-12-11T10:00:00.000Z",
            "billingEndDate": "2026-12-10T10:00:00.000Z"
        }

    return factory
