import pytest
from freezegun import freeze_time


@pytest.fixture
def invalid_order_id():
    return "ORD-0000-0000"


@pytest.fixture
@freeze_time("2025-12-01T10:00:00.000Z")
def order_factory(licensee_id, product_id, item_id):
    def factory(
        line_item_period: str = "1y",
        line_item_commitment: str = "1y",
        line_quantity: int = 10,
    ):
        return {
            "agreement": {
                "licensee": {"id": licensee_id},
                "product": {"id": product_id},
            },
            "type": "Purchase",
            "status": "Draft",
            "parameters": {
                "ordering": [
                    {
                        "id": f"{product_id}-0001",
                        "externalId": "agreementType",
                        "type": "Choice",
                        "constraints": {
                            "required": False,
                            "hidden": False,
                            "readonly": False,
                        },
                        "value": "New",
                    },
                    {
                        "id": f"{product_id}-0002",
                        "externalId": "companyName",
                        "type": "SingleLineText",
                        "constraints": {
                            "required": False,
                            "hidden": False,
                            "readonly": False,
                        },
                        "value": "Test Company",
                    },
                    {
                        "id": f"{product_id}-0003",
                        "externalId": "address",
                        "constraints": {
                            "required": False,
                            "hidden": False,
                            "readonly": False,
                        },
                        "value": {
                            "addressLine1": "123 Test St",
                            "city": "San Francisco",
                            "state": "CA",
                            "postCode": "12345",
                            "country": "US",
                        },
                    },
                ],
            },
            "lines": [
                {
                    "item": {
                        "id": item_id,
                        "terms": {
                            "model": "quantity",
                            "period": line_item_period,
                            "commitment": line_item_commitment,
                        }
                    },
                    "price": {
                        "currency": "USD",
                        "unitLP": 35.88,
                        "unitSP": 39.87,
                        "SPx1": None,
                        "SPxM": 27.55,
                        "SPxY": 330.55,
                    },
                    "quantity": line_quantity,
                }
            ]
        }
    return factory
