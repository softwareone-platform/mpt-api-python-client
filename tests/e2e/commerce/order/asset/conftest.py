import pytest


@pytest.fixture
def draft_order_asset_agreement_id(e2e_config):
    return e2e_config["commerce.assets.draft.order.agreement.id"]


@pytest.fixture
def asset_agreement_line_id(e2e_config):
    return e2e_config["commerce.assets.agreement.line.id"]


@pytest.fixture
def commerce_asset_draft_order_id(e2e_config):
    return e2e_config["commerce.assets.draft.order.id"]


@pytest.fixture
def order_asset_factory(
    draft_order_asset_agreement_id,
    buyer_id,
    asset_agreement_line_id,
    buyer_account_id,
    seller_id,
    commerce_product_id,
    commerce_asset_draft_order_id,
):
    def factory(
        name: str = "E2E Created Order Asset",
        quantity: int = 1,
        external_vendor_id: str = "ext-vendor-id",
    ):
        return {
            "name": name,
            "externalIds": {"vendor": external_vendor_id},
            "lines": [
                {
                    "id": asset_agreement_line_id,
                    "agreement": {"id": draft_order_asset_agreement_id},
                    "buyer": {"id": buyer_id},
                    "client": {"id": buyer_account_id},
                    "oldQuantity": 0,
                    "quantity": quantity,
                    "price": {
                        "unitPP": 10,
                        "PPx1": 100,
                        "currency": "USD",
                    },
                }
            ],
            "order": {"id": commerce_asset_draft_order_id},
            "product": {"id": commerce_product_id},
            "seller": {"id": seller_id},
        }

    return factory
