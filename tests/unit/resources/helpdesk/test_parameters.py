import pytest

from mpt_api_client.resources.helpdesk.parameters import (
    AsyncParametersService,
    ParametersService,
)


@pytest.fixture
def parameters_service(http_client):
    return ParametersService(http_client=http_client)


@pytest.fixture
def async_parameters_service(async_http_client):
    return AsyncParametersService(http_client=async_http_client)


def test_endpoint(parameters_service):
    result = parameters_service.path == "/public/v1/helpdesk/parameters"

    assert result is True


def test_async_endpoint(async_parameters_service):
    result = async_parameters_service.path == "/public/v1/helpdesk/parameters"

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "fetch_page", "iterate"])
def test_methods_present(parameters_service, method):
    result = hasattr(parameters_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "fetch_page", "iterate"])
def test_async_methods_present(async_parameters_service, method):
    result = hasattr(async_parameters_service, method)

    assert result is True
