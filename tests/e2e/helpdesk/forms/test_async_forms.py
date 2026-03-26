from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.forms import Form

pytestmark = [pytest.mark.flaky]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_get_form(async_mpt_ops, async_created_form):
    result = await async_mpt_ops.helpdesk.forms.get(async_created_form.id)

    assert result.id == async_created_form.id


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_list_forms(async_mpt_ops):
    result = await async_mpt_ops.helpdesk.forms.fetch_page(limit=1)

    assert len(result) > 0
    assert all(isinstance(form, Form) for form in result)


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_create_form(async_created_form):
    result = async_created_form

    assert result is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_update_form(async_mpt_ops, async_created_form, short_uuid):
    update_data = {"description": f"e2e update {short_uuid}"}

    result = await async_mpt_ops.helpdesk.forms.update(async_created_form.id, update_data)

    assert result.id == async_created_form.id
    assert result.to_dict().get("description") == update_data["description"]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_publish_form(async_mpt_ops, async_created_form):
    result = await async_mpt_ops.helpdesk.forms.publish(async_created_form.id)

    assert result is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_unpublish_form(async_mpt_ops, async_created_form):
    result = await async_mpt_ops.helpdesk.forms.unpublish(async_created_form.id)

    assert result is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_delete_form(async_mpt_ops, async_created_form):
    await async_mpt_ops.helpdesk.forms.delete(async_created_form.id)  # act


async def test_not_found(async_mpt_ops, invalid_form_id):
    with pytest.raises(MPTAPIError) as error:
        await async_mpt_ops.helpdesk.forms.get(invalid_form_id)
    assert error.value.status_code == HTTPStatus.NOT_FOUND
