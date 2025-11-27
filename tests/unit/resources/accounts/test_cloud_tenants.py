import pytest

from mpt_api_client.resources.accounts.cloud_tenants import (
    AsyncCloudTenantsService,
    CloudTenantsService,
)


@pytest.fixture
def cloud_tenants_service(http_client):
    return CloudTenantsService(http_client=http_client)


@pytest.fixture
def async_cloud_tenants_service(async_http_client):
    return AsyncCloudTenantsService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete"],
)
def test_cloud_tenants_mixins_present(cloud_tenants_service, method):
    result = hasattr(cloud_tenants_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete"],
)
def test_async_cloud_tenants_mixins_present(async_cloud_tenants_service, method):
    result = hasattr(async_cloud_tenants_service, method)

    assert result is True
