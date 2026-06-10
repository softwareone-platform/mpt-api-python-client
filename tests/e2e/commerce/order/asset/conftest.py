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
def order_asset_factory():

    def factory(
        order: dict,
        name: str = "E2E Created Order Asset",
        external_vendor_id: str = "ext-vendor-id",
    ):
        asset_lines = [line for line in order["lines"] if "Asset" in line["item"]["name"]]

        return {
            "name": name,
            "externalIds": {"vendor": external_vendor_id},
            "lines": asset_lines,
            "order": {"id": order["id"]},
            "product": {"id": order["product"]["id"]},
            "seller": {"id": order["seller"]["id"]},
        }

    return factory
