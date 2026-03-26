from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.parameter_groups import ParameterGroup

pytestmark = [
    pytest.mark.flaky,
    pytest.mark.skip(reason="Skipped per MPT-18373 request"),
]


def test_get_parameter_group(parameter_groups_service, created_parameter_group):
    result = parameter_groups_service.get(created_parameter_group.id)

    assert result.id == created_parameter_group.id


def test_list_parameter_groups(parameter_groups_service):
    result = parameter_groups_service.fetch_page(limit=1)

    assert len(result) > 0
    assert all(isinstance(parameter_group, ParameterGroup) for parameter_group in result)


def test_create_parameter_group(created_parameter_group):
    result = created_parameter_group

    assert result is not None


def test_update_parameter_group(parameter_groups_service, created_parameter_group, short_uuid):
    update_data = {"description": f"e2e update {short_uuid}"}

    result = parameter_groups_service.update(created_parameter_group.id, update_data)

    assert result.id == created_parameter_group.id
    assert result.to_dict().get("description") == update_data["description"]


def test_delete_parameter_group(parameter_groups_service, created_parameter_group):
    parameter_groups_service.delete(created_parameter_group.id)  # act


def test_not_found(parameter_groups_service, invalid_parameter_group_id):
    with pytest.raises(MPTAPIError) as error:
        parameter_groups_service.get(invalid_parameter_group_id)

    assert error.value.status_code == HTTPStatus.NOT_FOUND
