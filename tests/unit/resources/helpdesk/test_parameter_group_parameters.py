import pytest

from mpt_api_client.resources.helpdesk.parameter_group_parameters import (
    AsyncParameterGroupParametersService,
    ParameterGroupParametersService,
)


@pytest.fixture
def parameter_group_parameters_service(http_client):
    return ParameterGroupParametersService(
        http_client=http_client, endpoint_params={"group_id": "PGR-0000-0000"}
    )


@pytest.fixture
def async_parameter_group_parameters_service(async_http_client):
    return AsyncParameterGroupParametersService(
        http_client=async_http_client, endpoint_params={"group_id": "PGR-0000-0000"}
    )


def test_endpoint(parameter_group_parameters_service):
    result = (
        parameter_group_parameters_service.path
        == "/public/v1/helpdesk/parameter-groups/PGR-0000-0000/parameters"
    )

    assert result is True


def test_async_endpoint(async_parameter_group_parameters_service):
    result = (
        async_parameter_group_parameters_service.path
        == "/public/v1/helpdesk/parameter-groups/PGR-0000-0000/parameters"
    )

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "fetch_page", "iterate"],
)
def test_methods_present(parameter_group_parameters_service, method):
    result = hasattr(parameter_group_parameters_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "fetch_page", "iterate"],
)
def test_async_methods_present(async_parameter_group_parameters_service, method):
    result = hasattr(async_parameter_group_parameters_service, method)

    assert result is True
