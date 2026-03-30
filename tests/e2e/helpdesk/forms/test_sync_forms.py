from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.forms import Form

pytestmark = [pytest.mark.flaky]


def test_get_form(mpt_ops, created_form):
    result = mpt_ops.helpdesk.forms.get(created_form.id)

    assert result.id == created_form.id


def test_list_forms(mpt_ops):
    result = mpt_ops.helpdesk.forms.fetch_page(limit=1)

    assert len(result) > 0
    assert all(isinstance(form, Form) for form in result)


def test_create_form(created_form):
    result = created_form

    assert result is not None


def test_update_form(mpt_ops, created_form, short_uuid):
    update_data = {"description": f"e2e update {short_uuid}"}

    result = mpt_ops.helpdesk.forms.update(created_form.id, update_data)

    assert result.id == created_form.id
    assert result.to_dict().get("description") == update_data["description"]


def test_publish_form(mpt_ops, created_form):
    result = mpt_ops.helpdesk.forms.publish(created_form.id)

    assert result is not None


def test_unpublish_form(mpt_ops, created_published_form):
    result = mpt_ops.helpdesk.forms.unpublish(created_published_form.id)

    assert result.status == "Unpublished"


def test_delete_form(mpt_ops, created_form):
    mpt_ops.helpdesk.forms.delete(created_form.id)  # act


def test_not_found(mpt_ops, invalid_form_id):
    with pytest.raises(MPTAPIError) as error:
        mpt_ops.helpdesk.forms.get(invalid_form_id)

    assert error.value.status_code == HTTPStatus.NOT_FOUND
