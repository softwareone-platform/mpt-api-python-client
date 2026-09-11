import pytest

from mpt_api_client.resources.accounts.services import AsyncServicesService, ServicesService

SERVICES_PATH = "/public/v1/accounts/services"


@pytest.fixture
def services_service(http_client):
    return ServicesService(http_client=http_client)


@pytest.fixture
def async_services_service(async_http_client):
    return AsyncServicesService(http_client=async_http_client)


def test_endpoint(services_service):
    result = services_service.build_path()

    assert result == SERVICES_PATH


def test_async_endpoint(async_services_service):
    result = async_services_service.build_path()

    assert result == SERVICES_PATH


@pytest.mark.parametrize("method", ["get"])
def test_methods_present(services_service, method):
    result = hasattr(services_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get"])
def test_async_methods_present(async_services_service, method):
    result = hasattr(async_services_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["create", "update", "delete"])
def test_undocumented_methods_absent(services_service, method):
    result = hasattr(services_service, method)

    assert result is False


@pytest.mark.parametrize("method", ["create", "update", "delete"])
def test_async_undocumented_methods_absent(async_services_service, method):
    result = hasattr(async_services_service, method)

    assert result is False
