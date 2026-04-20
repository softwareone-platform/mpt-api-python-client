import pytest


@pytest.fixture
def variant_id(e2e_config):
    return e2e_config["program.terms.variant.id"]


@pytest.fixture
def invalid_variant_id():
    return "PTV-0000-0000-0000-0000"


@pytest.fixture
def variant_data_factory():
    def factory(variant_type: str = "File", asset_url: str = "") -> dict:
        return {
            "name": "E2E Created Program Term Variant",
            "description": "E2E Created Program Term Variant",
            "languageCode": "en-us",
            "type": variant_type,
            "assetUrl": asset_url,
        }

    return factory
