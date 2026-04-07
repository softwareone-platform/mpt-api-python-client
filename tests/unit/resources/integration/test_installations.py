import httpx
import pytest
import respx

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.integration.installations import (
    AsyncInstallationsService,
    Installation,
    InstallationsService,
)


@pytest.fixture
def installations_service(http_client):
    return InstallationsService(http_client=http_client)


@pytest.fixture
def async_installations_service(async_http_client):
    return AsyncInstallationsService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "create",
        "update",
        "delete",
        "invite",
        "install",
        "uninstall",
        "expire",
        "iterate",
    ],
)
def test_mixins_present(installations_service, method):
    result = hasattr(installations_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "create",
        "update",
        "delete",
        "invite",
        "install",
        "uninstall",
        "expire",
        "iterate",
    ],
)
def test_async_mixins_present(async_installations_service, method):
    result = hasattr(async_installations_service, method)

    assert result is True


@pytest.fixture
def installation_data():
    return {
        "id": "INS-001",
        "name": "My Installation",
        "revision": 2,
        "account": {"id": "ACC-001", "name": "Account"},
        "extension": {"id": "EXT-001", "name": "Extension"},
        "status": "Installed",
        "configuration": {"key": "value"},
        "invitation": {"url": "https://example.com/invite"},
        "modules": [{"id": "MOD-001"}],
        "terms": [{"id": "TERM-001"}],
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_installation_primitive_fields(installation_data):
    result = Installation(installation_data)

    assert result.id == "INS-001"
    assert result.name == "My Installation"
    assert result.revision == 2
    assert result.status == "Installed"


def test_installation_nested_fields(installation_data):
    result = Installation(installation_data)

    assert isinstance(result.account, BaseModel)
    assert isinstance(result.extension, BaseModel)
    assert isinstance(result.configuration, BaseModel)
    assert isinstance(result.invitation, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_installation_create(installations_service):
    installation_data = {
        "extension": {"id": "EXT-001"},
        "account": {"id": "ACC-001"},
    }
    expected_response = {"id": "INS-001", "name": "My Installation", "status": "Invited"}
    with respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/integration/installations").mock(
            return_value=httpx.Response(httpx.codes.CREATED, json=expected_response)
        )

        result = installations_service.create(installation_data)

    assert mock_route.call_count == 1
    assert mock_route.calls[0].request.method == "POST"
    assert result.to_dict() == expected_response
