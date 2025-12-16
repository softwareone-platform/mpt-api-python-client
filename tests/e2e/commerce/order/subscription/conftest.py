import pytest
from freezegun import freeze_time


@pytest.fixture
def order_subscription_factory(agreement_subscription_line_id):
    @freeze_time("2025-11-14T09:00:00.000Z")
    def factory(
        name: str = "E2E Created Order Subscription",
        external_vendor_id: str = "ext-vendor-id",
    ):
        return {
            "name": name,
            "startDate": "2025-11-03T09:00:00.000Z",
            "commitmentDate": "2026-11-02T09:00:00.000Z",
            "autoRenew": True,
            "externalIds": {"vendor": external_vendor_id},
            "template": None,
            "lines": [{"id": agreement_subscription_line_id}],
            "parameters": {"fulfillment": []},
        }

    return factory
