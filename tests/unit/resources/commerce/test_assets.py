import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.commerce.assets import Asset, AssetService, AsyncAssetService


@pytest.fixture
def assets_service(http_client):
    return AssetService(http_client=http_client)


@pytest.fixture
def async_assets_service(async_http_client):
    return AsyncAssetService(http_client=async_http_client)


@pytest.mark.parametrize("method", ["create", "update", "get", "render", "terminate"])
def test_assets_service_methods(assets_service, method):
    result = hasattr(assets_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["create", "update", "get", "render", "terminate"])
def test_async_assets_service_methods(async_assets_service, method):
    result = hasattr(async_assets_service, method)

    assert result is True


@pytest.fixture
def asset_data():
    return {
        "id": "ASS-001",
        "name": "My Asset",
        "status": "Active",
        "externalIds": {"vendor": "ext-001"},
        "price": {"total": 100},
        "template": {"id": "TPL-001"},
        "parameters": {"fulfillment": []},
        "terms": {"id": "TRM-001"},
        "agreement": {"id": "AGR-001"},
        "product": {"id": "PRD-001"},
        "priceList": {"id": "PRL-001"},
        "listing": {"id": "LST-001"},
        "licensee": {"id": "ACC-001"},
        "lines": [{"id": "LIN-001"}],
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_asset_primitive_fields(asset_data):
    result = Asset(asset_data)

    assert result.to_dict() == asset_data


def test_asset_nested_pricing_fields(asset_data):  # noqa: WPS218
    result = Asset(asset_data)

    assert isinstance(result.external_ids, BaseModel)
    assert isinstance(result.price, BaseModel)
    assert isinstance(result.template, BaseModel)
    assert isinstance(result.parameters, BaseModel)
    assert isinstance(result.terms, BaseModel)


def test_asset_nested_relation_fields(asset_data):  # noqa: WPS218
    result = Asset(asset_data)

    assert isinstance(result.agreement, BaseModel)
    assert isinstance(result.product, BaseModel)
    assert isinstance(result.price_list, BaseModel)
    assert isinstance(result.listing, BaseModel)
    assert isinstance(result.licensee, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_asset_optional_fields_absent():
    result = Asset({"id": "ASS-001"})

    assert result.id == "ASS-001"
    assert not hasattr(result, "name")
    assert not hasattr(result, "status")
    assert not hasattr(result, "audit")
