import pytest


@pytest.fixture
def authorizations_service(mpt_ops):
    return mpt_ops.catalog.authorizations


@pytest.fixture
def authorization_data(product_id, seller_id, account_id, short_uuid):
    return {
        "externalIds": {"operations": f"e2e-{short_uuid}"},
        "product": {"id": product_id},
        "owner": {"id": seller_id},
        "journal": {"firstInvoiceDate": "2025-12-01", "frequency": "1m"},
        "eligibility": {"client": True, "partner": True},
        "currency": "USD",
        "notes": "e2e - please delete",
        "name": "e2e - please delete",
        "vendor": {"id": account_id},
    }
