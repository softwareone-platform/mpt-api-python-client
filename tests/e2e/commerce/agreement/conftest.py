import pytest
from freezegun import freeze_time


@pytest.fixture
def invalid_agreement_id():
    return "AGR-0000-0000"


@pytest.fixture
def agreement_factory(  # noqa: WPS211
    account_id,
    seller_id,
    buyer_id,
    licensee_id,
    commerce_product_id,
    authorization_id,
):
    @freeze_time("2025-11-14T09:00:00.000Z")
    def factory(
        name: str = "E2E Created Agreement",
        client_external_id: str = "test-client-external-id",
        vendor_external_id: str = "test-vendor-external-id",
    ):
        return {
            "name": name,
            "status": "Active",
            "vendor": {"id": account_id},
            "authorization": {"id": authorization_id},
            "seller": {"id": seller_id},
            "buyer": {"id": buyer_id},
            "licensee": {"id": licensee_id},
            "product": {"id": commerce_product_id},
            "value": {
                "PPxY": 150,
                "PPxM": 12.5,
                "SPxY": 165,
                "SPxM": 13.75,
                "markup": 0.1,
                "margin": 0.11,
                "currency": "USD",
            },
            "startDate": "2025-11-14T09:00:00.000Z",
            "endDate": "2026-11-13T09:00:00.000Z",
            "externalIds": {
                "client": client_external_id,
                "vendor": vendor_external_id,
            },
        }

    return factory
