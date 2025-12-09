import pytest
from freezegun import freeze_time


@pytest.fixture
def subscription_id(e2e_config):
    return e2e_config["commerce.subscription.id"]


@pytest.fixture
def invalid_subscription_id():
    return "SUB-0000-0000-0000"


@pytest.fixture
def subscription_factory(subscription_agreement_id, subscription_item_id):
    @freeze_time("2025-11-14T09:00:00.000Z")
    def factory(
        name: str = "E2E Created Subscription",
        external_vendor_id: str = "ext-vendor-id",
        quantity: int = 1,
    ):
        return {
            "name": name,
            "startDate": "2025-11-03T09:00:00.000Z",
            "commitmentDate": "2026-11-02T09:00:00.000Z",
            "autoRenew": True,
            "agreement": {"id": subscription_agreement_id},
            "externalIds": {"vendor": external_vendor_id},
            "template": None,
            "lines": [
                {
                    "item": {"id": subscription_item_id},
                    "quantity": quantity,
                    "price": {"unitPP": 10},
                }
            ],
            "parameters": {"fulfillment": []},
        }

    return factory
