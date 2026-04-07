from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.parameters import Parameter

pytestmark = [pytest.mark.flaky, pytest.mark.skip(reason="Unskip after MPT-19967 fixed")]


async def test_get_parameter(async_mpt_ops, async_created_parameter):
    result = await async_mpt_ops.helpdesk.parameters.get(async_created_parameter.id)

    assert isinstance(result, Parameter)


async def test_list_parameters(async_mpt_ops):
    result = await async_mpt_ops.helpdesk.parameters.fetch_page(limit=1)

    assert len(result) > 0
    assert all(isinstance(parameter, Parameter) for parameter in result)


def test_create_parameter(async_created_parameter):
    result = async_created_parameter

    assert isinstance(result, Parameter)


async def test_update_parameter(async_mpt_ops, async_created_parameter, short_uuid):
    update_data = {"description": f"e2e update {short_uuid}"}

    result = await async_mpt_ops.helpdesk.parameters.update(async_created_parameter.id, update_data)

    assert isinstance(result, Parameter)
    assert result.to_dict().get("description") == update_data["description"]


async def test_delete_parameter(async_mpt_ops, async_created_parameter):
    await async_mpt_ops.helpdesk.parameters.delete(async_created_parameter.id)  # act


async def test_not_found(async_mpt_ops, invalid_parameter_id):
    with pytest.raises(MPTAPIError) as error:
        await async_mpt_ops.helpdesk.parameters.get(invalid_parameter_id)
    assert error.value.status_code == HTTPStatus.NOT_FOUND
