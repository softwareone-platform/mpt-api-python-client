import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [
    pytest.mark.flaky,
    pytest.mark.skip(reason="Skipped per MPT-18373 request"),
]


def test_get_parameter(mpt_ops, created_parameter):
    result = mpt_ops.helpdesk.parameters.get(created_parameter.id)

    assert result.id == created_parameter.id


def test_list_parameters(mpt_ops):
    result = mpt_ops.helpdesk.parameters.fetch_page(limit=1)

    assert len(result) > 0


def test_create_parameter(created_parameter):
    result = created_parameter

    assert result is not None


def test_update_parameter(mpt_ops, created_parameter, short_uuid):
    update_data = {"description": f"e2e update {short_uuid}"}

    result = mpt_ops.helpdesk.parameters.update(created_parameter.id, update_data)

    assert result.id == created_parameter.id
    assert result.to_dict().get("description") == update_data["description"]


def test_delete_parameter(mpt_ops, created_parameter):
    mpt_ops.helpdesk.parameters.delete(created_parameter.id)  # act


def test_not_found(mpt_ops, invalid_parameter_id):
    with pytest.raises(MPTAPIError):
        mpt_ops.helpdesk.parameters.get(invalid_parameter_id)
