import pytest


@pytest.fixture
def agreement_asset_id(e2e_config):
    return e2e_config["commerce.assets.id"]


@pytest.fixture
def invalid_agreement_asset_id():
    return "AST-0000-0000-0000"


@pytest.fixture
def asset_factory(asset_item_id, asset_agreement_id):
    def factory(
        name: str = "E2E Created Asset",
        quantity: int = 1,
        external_vendor_id: str = "ext-vendor-id",
    ):
        return {
            "name": name,
            "agreement": {"id": asset_agreement_id},
            "externalIds": {"vendor": external_vendor_id},
            "lines": [
                {
                    "item": {"id": asset_item_id},
                    "quantity": quantity,
                    "price": {
                        "unitPP": 10,
                        "PPx12": 10,
                    },
                }
            ],
        }

    return factory
