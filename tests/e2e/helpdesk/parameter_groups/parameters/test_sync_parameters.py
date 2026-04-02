from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.parameter_group_parameters import ParameterGroupParameter

pytestmark = [
    pytest.mark.flaky,
    pytest.mark.skip(reason="Skipped per MPT-18373 request"),
]


def test_get_parameter_group_parameter(
    parameter_group_parameters_service, created_parameter_group_parameter
):
    result = parameter_group_parameters_service.get(created_parameter_group_parameter.id)

    assert isinstance(result, ParameterGroupParameter)


def test_list_parameter_group_parameters(
    parameter_group_parameters_service, created_parameter_group_parameter
):
    result = parameter_group_parameters_service.fetch_page(limit=20)

    assert len(result) > 0
    assert all(isinstance(parameter, ParameterGroupParameter) for parameter in result)
    assert any(parameter.id == created_parameter_group_parameter.id for parameter in result)


def test_create_parameter_group_parameter(created_parameter_group_parameter):
    result = created_parameter_group_parameter

    assert isinstance(result, ParameterGroupParameter)


def test_update_parameter_group_parameter(
    parameter_group_parameters_service, created_parameter_group_parameter
):
    update_data = {"displayOrder": 101}

    result = parameter_group_parameters_service.update(
        created_parameter_group_parameter.id, update_data
    )

    assert isinstance(result, ParameterGroupParameter)
    assert result.to_dict().get("displayOrder") == update_data["displayOrder"]


def test_delete_parameter_group_parameter(
    parameter_group_parameters_service, created_parameter_group_parameter
):
    parameter_group_parameters_service.delete(created_parameter_group_parameter.id)  # act


def test_not_found(parameter_group_parameters_service, invalid_parameter_group_parameter_id):
    with pytest.raises(MPTAPIError) as error:
        parameter_group_parameters_service.get(invalid_parameter_group_parameter_id)

    assert error.value.status_code == HTTPStatus.NOT_FOUND
