import httpx
import pytest
import respx

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.integration.extension_instances import (
    AsyncExtensionInstancesService,
    ExtensionInstance,
    ExtensionInstancesService,
)
from mpt_api_client.resources.integration.extensions import (
    AsyncExtensionsService,
    ExtensionsService,
)


@pytest.fixture
def extension_instances_service(http_client):
    return ExtensionInstancesService(
        http_client=http_client, endpoint_params={"extension_id": "EXT-001"}
    )


@pytest.fixture
def async_extension_instances_service(async_http_client):
    return AsyncExtensionInstancesService(
        http_client=async_http_client, endpoint_params={"extension_id": "EXT-001"}
    )


@pytest.fixture
def extensions_service(http_client):
    return ExtensionsService(http_client=http_client)


@pytest.fixture
def async_extensions_service(async_http_client):
    return AsyncExtensionsService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "create",
        "iterate",
    ],
)
def test_mixins_present(extension_instances_service, method):
    result = hasattr(extension_instances_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "create",
        "iterate",
    ],
)
def test_async_mixins_present(async_extension_instances_service, method):
    result = hasattr(async_extension_instances_service, method)

    assert result is True


def test_extension_instance_primitive_fields():
    instance_data = {
        "id": "INS-001",
        "name": "My Instance",
        "revision": 2,
        "externalId": "ext-123",
        "status": "Running",
        "extension": {"id": "EXT-001"},
        "meta": {"id": "META-001"},
        "channel": {"type": "grpc"},
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }

    result = ExtensionInstance(instance_data)

    assert result.id == "INS-001"
    assert result.name == "My Instance"
    assert result.revision == 2
    assert result.external_id == "ext-123"
    assert result.status == "Running"
    assert isinstance(result.extension, BaseModel)
    assert isinstance(result.meta, BaseModel)
    assert isinstance(result.channel, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_extension_instance_create(extension_instances_service):
    payload = {"externalId": "ext-123", "version": "1.0.0", "channel": {"type": "grpc"}}
    expected_response = {"id": "INS-001", "name": "My Instance", "status": "Connecting"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/integration/extensions/EXT-001/instances"
        ).mock(return_value=httpx.Response(httpx.codes.CREATED, json=expected_response))

        result = extension_instances_service.create(payload)

    assert mock_route.call_count == 1
    assert mock_route.calls[0].request.method == "POST"
    assert result.to_dict() == expected_response


def test_extension_instances_list(extension_instances_service):
    expected_response = {
        "data": [
            {"id": "INS-001", "name": "Instance 1", "status": "Running"},
            {"id": "INS-002", "name": "Instance 2", "status": "Disconnected"},
        ]
    }
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/integration/extensions/EXT-001/instances"
        ).mock(return_value=httpx.Response(httpx.codes.OK, json=expected_response))

        result = list(extension_instances_service.iterate())

    assert mock_route.call_count == 1
    assert len(result) == 2
    assert result[0].id == "INS-001"
    assert result[1].id == "INS-002"


def test_extensions_instances_accessor(extensions_service, http_client):
    result = extensions_service.instances("EXT-001")

    assert isinstance(result, ExtensionInstancesService)
    assert result.http_client is http_client


def test_async_extensions_instances_accessor(async_extensions_service, async_http_client):
    result = async_extensions_service.instances("EXT-001")

    assert isinstance(result, AsyncExtensionInstancesService)
    assert result.http_client is async_http_client
