import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.catalog.authorizations import (
    AsyncAuthorizationsService,
    Authorization,
    AuthorizationsService,
)


@pytest.fixture
def authorizations_service(http_client):
    return AuthorizationsService(http_client=http_client)


@pytest.fixture
def async_authorizations_service(async_http_client):
    return AsyncAuthorizationsService(http_client=async_http_client)


@pytest.fixture
def authorization_data():
    return {
        "id": "AUT-001",
        "name": "My Authorization",
        "currency": "USD",
        "notes": "Some notes",
        "externalIds": {"vendor": "ext-001"},
        "product": {"id": "PRD-001", "name": "My Product"},
        "vendor": {"id": "ACC-001", "name": "Vendor"},
        "owner": {"id": "ACC-002", "name": "Owner"},
        "statistics": {"items": 5},
        "journal": {"id": "JRN-001"},
        "eligibility": {"status": "Eligible"},
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate"])
def test_mixins_present(authorizations_service, method):
    result = hasattr(authorizations_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate"])
def test_async_mixins_present(async_authorizations_service, method):
    result = hasattr(async_authorizations_service, method)

    assert result is True


def test_authorization_primitive_fields(authorization_data):
    result = Authorization(authorization_data)

    assert result.to_dict() == authorization_data


def test_authorization_nested_base_models(authorization_data):
    result = Authorization(authorization_data)

    assert isinstance(result.external_ids, BaseModel)
    assert isinstance(result.product, BaseModel)
    assert isinstance(result.vendor, BaseModel)
    assert isinstance(result.statistics, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_authorization_optional_fields_absent():
    result = Authorization({"id": "AUT-001"})

    assert result.id == "AUT-001"
    assert not hasattr(result, "name")
    assert not hasattr(result, "currency")
    assert not hasattr(result, "audit")
