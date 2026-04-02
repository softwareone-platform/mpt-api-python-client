from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.parameter_group_parameters import ParameterGroupParameter

pytestmark = [
    pytest.mark.flaky,
    pytest.mark.skip(reason="Skipped per MPT-18373 request"),
]


async def test_get_parameter_group_parameter(
    async_parameter_group_parameters_service, async_created_parameter_group_parameter
):
    result = await async_parameter_group_parameters_service.get(
        async_created_parameter_group_parameter.id
    )

    assert isinstance(result, ParameterGroupParameter)


async def test_list_parameter_group_parameters(
    async_parameter_group_parameters_service, async_created_parameter_group_parameter
):
    result = await async_parameter_group_parameters_service.fetch_page(limit=20)

    assert len(result) > 0
    assert all(isinstance(parameter, ParameterGroupParameter) for parameter in result)
    assert any(parameter.id == async_created_parameter_group_parameter.id for parameter in result)


def test_create_parameter_group_parameter(async_created_parameter_group_parameter):
    result = async_created_parameter_group_parameter

    assert isinstance(result, ParameterGroupParameter)


async def test_update_parameter_group_parameter(
    async_parameter_group_parameters_service, async_created_parameter_group_parameter
):
    update_data = {"displayOrder": 101}

    result = await async_parameter_group_parameters_service.update(
        async_created_parameter_group_parameter.id,
        update_data,
    )

    assert isinstance(result, ParameterGroupParameter)
    assert result.to_dict().get("displayOrder") == update_data["displayOrder"]


async def test_delete_parameter_group_parameter(
    async_parameter_group_parameters_service, async_created_parameter_group_parameter
):
    await async_parameter_group_parameters_service.delete(
        async_created_parameter_group_parameter.id
    )  # act


async def test_not_found(
    async_parameter_group_parameters_service, invalid_parameter_group_parameter_id
):
    with pytest.raises(MPTAPIError) as error:
        await async_parameter_group_parameters_service.get(invalid_parameter_group_parameter_id)
    assert error.value.status_code == HTTPStatus.NOT_FOUND
