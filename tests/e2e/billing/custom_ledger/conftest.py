import pathlib

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
    seller_id,
    account_id,
):
    def factory(
        name: str = "E2E Created Custom Ledger",
        notes: str = "E2E Created Custom Ledger",
    ):
        return {
            "name": name,
            "seller": {"id": seller_id},
            "vendor": {"id": account_id},
            "price": {
                "currency": {
                    "purchase": "USD",
                    "sale": "USD",
                },
            },
            "notes": notes,
            "billingStartDate": "2025-12-01T07:00:00.000Z",
            "billingEndDate": "2026-11-30T07:00:00.000Z",
            "externalIds": {},
        }

    return factory


@pytest.fixture
def billing_custom_ledger_fd():
    file_path = pathlib.Path("tests/data/test_custom_ledger.xlsx").resolve()
    fd = file_path.open("rb")
    try:
        yield fd
    finally:
        fd.close()
