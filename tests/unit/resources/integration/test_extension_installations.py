import httpx
import pytest
import respx

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.integration.extension_installations import (
    AsyncExtensionInstallationsService,
    ExtensionInstallation,
    ExtensionInstallationsService,
)
from mpt_api_client.resources.integration.extensions import (
    AsyncExtensionsService,
    ExtensionsService,
)


@pytest.fixture
def extension_installations_service(http_client):
    return ExtensionInstallationsService(
        http_client=http_client, endpoint_params={"extension_id": "EXT-001"}
    )


@pytest.fixture
def async_extension_installations_service(async_http_client):
    return AsyncExtensionInstallationsService(
        http_client=async_http_client, endpoint_params={"extension_id": "EXT-001"}
    )


@pytest.fixture
def extensions_service(http_client):
    return ExtensionsService(http_client=http_client)


@pytest.fixture
def async_extensions_service(async_http_client):
    return AsyncExtensionsService(http_client=async_http_client)


@pytest.mark.parametrize("method", ["get", "iterate"])
def test_mixins_present(extension_installations_service, method):
    result = hasattr(extension_installations_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "iterate"])
def test_async_mixins_present(async_extension_installations_service, method):
    result = hasattr(async_extension_installations_service, method)

    assert result is True


def test_endpoint(extension_installations_service):
    result = (
        extension_installations_service.path
        == "/public/v1/integration/extensions/EXT-001/installations"
    )

    assert result is True


def test_async_endpoint(async_extension_installations_service):
    result = (
        async_extension_installations_service.path
        == "/public/v1/integration/extensions/EXT-001/installations"
    )

    assert result is True


@pytest.fixture
def installation_data():
    return {
        "id": "INST-001",
        "name": "My Installation",
        "revision": 2,
        "account": {"id": "ACC-001", "name": "Test Account"},
        "extension": {"id": "EXT-001", "name": "My Extension"},
        "status": "Installed",
        "configuration": {"key": "value"},
        "invitation": {"token": "abc123"},
        "modules": [{"id": "MOD-001"}],
        "terms": [{"id": "TERM-001"}],
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_extension_installation_primitive_fields(installation_data):
    result = ExtensionInstallation(installation_data)

    assert result.id == "INST-001"
    assert result.name == "My Installation"
    assert result.revision == 2
    assert result.status == "Installed"


def test_installation_nested_fields(installation_data):
    result = ExtensionInstallation(installation_data)

    assert isinstance(result.account, BaseModel)
    assert isinstance(result.extension, BaseModel)
    assert isinstance(result.configuration, BaseModel)
    assert isinstance(result.invitation, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_installation_optional_fields_absent():
    result = ExtensionInstallation({"id": "INST-001"})

    assert result.id == "INST-001"
    assert not hasattr(result, "name")
    assert not hasattr(result, "status")
    assert not hasattr(result, "audit")


def test_extension_installations_list(extension_installations_service):
    expected_response = {
        "data": [
            {"id": "INST-001", "name": "Installation One", "status": "Installed"},
            {"id": "INST-002", "name": "Installation Two", "status": "Invited"},
        ]
    }
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/integration/extensions/EXT-001/installations"
        ).mock(return_value=httpx.Response(httpx.codes.OK, json=expected_response))

        result = list(extension_installations_service.iterate())

    assert mock_route.call_count == 1
    assert len(result) == 2
    assert result[0].id == "INST-001"
    assert result[1].id == "INST-002"


def test_extension_installation_get(extension_installations_service):
    expected_response = {"id": "INST-001", "name": "My Installation", "status": "Installed"}
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/integration/extensions/EXT-001/installations/INST-001"
        ).mock(return_value=httpx.Response(httpx.codes.OK, json=expected_response))

        result = extension_installations_service.get("INST-001")

    assert mock_route.call_count == 1
    assert result.id == "INST-001"
    assert result.name == "My Installation"
    assert result.status == "Installed"


def test_extensions_installations_accessor(extensions_service, http_client):
    result = extensions_service.installations("EXT-001")

    assert isinstance(result, ExtensionInstallationsService)
    assert result.http_client is http_client
    assert result.endpoint_params == {"extension_id": "EXT-001"}


def test_async_extensions_installations_accessor(async_extensions_service, async_http_client):
    result = async_extensions_service.installations("EXT-001")

    assert isinstance(result, AsyncExtensionInstallationsService)
    assert result.http_client is async_http_client
    assert result.endpoint_params == {"extension_id": "EXT-001"}
