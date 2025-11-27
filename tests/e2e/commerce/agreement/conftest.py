import datetime as dt

import pytest
from dateutil.relativedelta import relativedelta
from freezegun import freeze_time

from mpt_api_client.utils import get_iso_dt_str


@pytest.fixture
def invalid_agreement_id():
    return "AGR-0000-0000"


@pytest.fixture
def agreement_factory(
    account_id,
    seller_id,
    buyer_id,
    licensee_id,
    product_id,
    template_id,
):
    @freeze_time("2025-11-14T09:00:00.000Z")
    def _agreement_factory(
        name: str = "E2E Seeded Agreement",
        external_operations_id: str = "e2e-ext-ops-id-12345",
    ):
        """Factory to create agreement data."""
        start_date = dt.datetime.now(tz=dt.UTC)
        end_date = start_date + relativedelta(years=1)

        return {
            "name": name,
            "status": "Active",
            "client": {"id": account_id},
            "seller": {"id": seller_id},
            "buyer": {"id": buyer_id},
            "licensee": {"id": licensee_id},
            "product": {"id": product_id},
            "value": {
                "PPxY": 150,
                "PPxM": 12.50,
                "SPxY": 165,
                "SPxM": 13.75,
                "markup": 0.10,
                "margin": 0.11,
                "currency": "USD"
            },
            "startDate": get_iso_dt_str(start_date),
            "endDate": get_iso_dt_str(end_date),
            "template": {"id": template_id},
            "externalIDs": {"operations":	external_operations_id}
        }
    return _agreement_factory
