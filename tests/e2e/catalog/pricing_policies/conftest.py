import pytest


@pytest.fixture
def buyer_id(e2e_config):
    return e2e_config["accounts.buyer.account.id"]


@pytest.fixture
def pricing_policy_data(buyer_id, product_id):
    return {
        "name": "e2e - pricing policy please delete",
        "description": "Test pricing policy description",
        "client": {"id": buyer_id},
        "product": {"id": product_id},
        "eligibility": {"client": True, "partner": False},
        "margin": "0.20",
    }


@pytest.fixture
def pricing_policy_id(e2e_config):
    return e2e_config.get("catalog.pricing_policy.id")
