import pytest

from mpt_api_client.resources.helpdesk.parameter_group_parameters import (
    AsyncParameterGroupParametersService,
    ParameterGroupParametersService,
)
from mpt_api_client.resources.helpdesk.parameter_groups import (
    AsyncParameterGroupsService,
    ParameterGroupsService,
)


@pytest.fixture
def parameter_groups_service(http_client):
    return ParameterGroupsService(http_client=http_client)


@pytest.fixture
def async_parameter_groups_service(async_http_client):
    return AsyncParameterGroupsService(http_client=async_http_client)


def test_endpoint(parameter_groups_service):
    result = parameter_groups_service.path == "/public/v1/helpdesk/parameter-groups"

    assert result is True


def test_async_endpoint(async_parameter_groups_service):
    result = async_parameter_groups_service.path == "/public/v1/helpdesk/parameter-groups"

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "fetch_page", "iterate", "parameters"],
)
def test_methods_present(parameter_groups_service, method):
    result = hasattr(parameter_groups_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "fetch_page", "iterate", "parameters"],
)
def test_async_methods_present(async_parameter_groups_service, method):
    result = hasattr(async_parameter_groups_service, method)

    assert result is True


def test_parameters_service(parameter_groups_service):
    result = parameter_groups_service.parameters("PGR-0000-0000")

    assert isinstance(result, ParameterGroupParametersService)
    assert result.endpoint_params == {"group_id": "PGR-0000-0000"}


def test_async_parameters_service(async_parameter_groups_service):
    result = async_parameter_groups_service.parameters("PGR-0000-0000")

    assert isinstance(result, AsyncParameterGroupParametersService)
    assert result.endpoint_params == {"group_id": "PGR-0000-0000"}
