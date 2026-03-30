import pytest

from tests.e2e.helper import (
    async_create_fixture_resource_and_delete,
    create_fixture_resource_and_delete,
)


@pytest.fixture
def form_data(short_uuid):
    return {
        "name": f"E2E Helpdesk Form {short_uuid}",
        "description": "E2E Created Helpdesk Form",
    }


@pytest.fixture(scope="session")
def invalid_form_id():
    return "FRM-0000-0000"


@pytest.fixture
def created_form(mpt_ops, form_data):
    with create_fixture_resource_and_delete(mpt_ops.helpdesk.forms, form_data) as form:
        yield form


@pytest.fixture
def created_published_form(mpt_ops, created_form):
    mpt_ops.helpdesk.forms.publish(created_form.id)
    return created_form


@pytest.fixture
async def async_created_form(async_mpt_ops, form_data):
    async with async_create_fixture_resource_and_delete(
        async_mpt_ops.helpdesk.forms, form_data
    ) as form:
        yield form


@pytest.fixture
async def async_created_published_form(async_mpt_ops, async_created_form):
    await async_mpt_ops.helpdesk.forms.publish(async_created_form.id)
    return async_created_form
