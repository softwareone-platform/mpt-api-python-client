import pytest


@pytest.fixture
def variant_data():
    return {
        "name": "e2e - please delete",
        "description": "Test variant description",
        "languageCode": "en-gb",
        "type": "File",
        "assetUrl": "",
    }


@pytest.fixture
def variant_id(e2e_config):
    return e2e_config["catalog.product.terms.variant.id"]
