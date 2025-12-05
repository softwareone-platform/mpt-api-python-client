import pytest
from freezegun import freeze_time


@pytest.fixture
def invalid_order_id():
    return "ORD-0000-0000"


@pytest.fixture
@freeze_time("2025-12-01T10:00:00.000Z")
def order_factory(licensee_id, commerce_product_id, commerce_item_id, authorization_id):
    def factory(
        notes: str = "E2E Created Order",
        line_item_period: str = "1y",
        line_item_commitment: str = "1y",
        line_quantity: int = 10,
    ):
        return {
            "agreement": {
                "licensee": {"id": licensee_id},
                "product": {"id": commerce_product_id},
            },
            "authorization": {"id": authorization_id},
            "type": "Purchase",
            "status": "Draft",
            "parameters": {
                "ordering": [],
                "fulfillment": [],
            },
            "notes": notes,
            "lines": [
                {
                    "item": {
                        "id": commerce_item_id,
                        "terms": {
                            "model": "quantity",
                            "period": line_item_period,
                            "commitment": line_item_commitment,
                        },
                    },
                    "price": {
                        "currency": "USD",
                        "unitSP": 15,
                        "SPx1": None,
                        "SPxM": 1.25,
                        "SPxY": 15,
                    },
                    "quantity": line_quantity,
                }
            ],
        }

    return factory


@pytest.fixture
def order_subscription_factory():
    def factory(
        line_id: str,
        name: str = "E2E Created Order Subscription",
    ):
        return {
            "name": name,
            "parameters": {"fulfillment": []},
            "lines": [{"id": line_id}],
            "terms": {"model": "quantity", "period": "1y", "commitment": "1y"},
            "autoRenew": True,
            "template": None,
        }

    return factory
