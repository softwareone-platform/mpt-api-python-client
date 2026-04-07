from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.parameters import Parameter

pytestmark = [pytest.mark.flaky, pytest.mark.skip(reason="Unskip after MPT-19967 fixed")]


def test_get_parameter(mpt_ops, created_parameter):
    result = mpt_ops.helpdesk.parameters.get(created_parameter.id)

    assert isinstance(result, Parameter)


def test_list_parameters(mpt_ops):
    result = mpt_ops.helpdesk.parameters.fetch_page(limit=1)

    assert len(result) > 0
    assert all(isinstance(parameter, Parameter) for parameter in result)


def test_create_parameter(created_parameter):
    result = created_parameter

    assert isinstance(result, Parameter)


def test_update_parameter(mpt_ops, created_parameter, short_uuid):
    update_data = {"description": f"e2e update {short_uuid}"}

    result = mpt_ops.helpdesk.parameters.update(created_parameter.id, update_data)

    assert isinstance(result, Parameter)
    assert result.to_dict().get("description") == update_data["description"]


def test_delete_parameter(mpt_ops, created_parameter):
    mpt_ops.helpdesk.parameters.delete(created_parameter.id)  # act


def test_not_found(mpt_ops, invalid_parameter_id):
    with pytest.raises(MPTAPIError) as error:
        mpt_ops.helpdesk.parameters.get(invalid_parameter_id)

    assert error.value.status_code == HTTPStatus.NOT_FOUND
