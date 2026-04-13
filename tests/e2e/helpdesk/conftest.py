import pytest

from tests.e2e.helper import (
    async_create_fixture_resource_and_delete,
    create_fixture_resource_and_delete,
)


@pytest.fixture
def queue_data(short_uuid):
    return {
        "name": f"E2E Queue {short_uuid}",
        "description": "E2E Created Helpdesk Queue",
        "internal": False,
    }


@pytest.fixture(scope="session")
def invalid_queue_id():
    return "HQU-0000-0000"


@pytest.fixture
def created_queue(mpt_ops, queue_data):
    with create_fixture_resource_and_delete(mpt_ops.helpdesk.queues, queue_data) as queue:
        yield queue


@pytest.fixture
def created_disabled_queue(mpt_ops, created_queue):
    result = mpt_ops.helpdesk.queues.disable(created_queue.id)
    assert result.status == "Disabled"

    return result


@pytest.fixture
async def async_created_queue(async_mpt_ops, queue_data):
    async with async_create_fixture_resource_and_delete(
        async_mpt_ops.helpdesk.queues, queue_data
    ) as queue:
        yield queue


@pytest.fixture
async def async_created_disabled_queue(async_mpt_ops, async_created_queue):
    result = await async_mpt_ops.helpdesk.queues.disable(async_created_queue.id)
    assert result.status == "Disabled"

    return result


@pytest.fixture(scope="session")
def invalid_case_id():
    return "CAS-0000-0000"


@pytest.fixture
def case_data(created_queue):
    return {
        "queue": {"id": created_queue.id},
        "chat": {"lastMessage": {"content": "E2E testing!!!"}},
    }


@pytest.fixture
def created_case(mpt_ops, case_data):
    return mpt_ops.helpdesk.cases.create(case_data)


@pytest.fixture
def queried_case(mpt_ops, created_case):
    return mpt_ops.helpdesk.cases.query(created_case.id, {"queryPrompt": "More details needed"})


@pytest.fixture
def processed_case(mpt_ops, queried_case):
    return mpt_ops.helpdesk.cases.process(queried_case.id)


@pytest.fixture
def created_chat(created_case):
    return created_case.chat


@pytest.fixture
async def async_created_case(async_mpt_ops, case_data):
    return await async_mpt_ops.helpdesk.cases.create(case_data)


@pytest.fixture
async def async_queried_case(async_mpt_ops, async_created_case):
    return await async_mpt_ops.helpdesk.cases.query(
        async_created_case.id, {"queryPrompt": "More details needed"}
    )


@pytest.fixture
async def async_processed_case(async_mpt_ops, async_queried_case):
    return await async_mpt_ops.helpdesk.cases.process(async_queried_case.id)


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
    return mpt_ops.helpdesk.forms.publish(created_form.id)


@pytest.fixture
async def async_created_form(async_mpt_ops, form_data):
    async with async_create_fixture_resource_and_delete(
        async_mpt_ops.helpdesk.forms, form_data
    ) as form:
        yield form


@pytest.fixture
async def async_created_published_form(async_mpt_ops, async_created_form):
    return await async_mpt_ops.helpdesk.forms.publish(async_created_form.id)


@pytest.fixture
def parameter_data(short_uuid):
    return {
        "name": f"E2E Helpdesk Parameter {short_uuid}",
        "description": "E2E Created Helpdesk Parameter",
        "scope": "Form",
        "phase": "Request",
        "type": "SingleLineText",
        "multiple": False,
        "displayOrder": None,
        "constraints": {
            "required": False,
            "readonly": False,
            "hidden": False,
        },
        "options": {
            "hintText": "E2E Parameter Hint Text",
            "placeholderText": "E2E Parameter Placeholder Text",
        },
    }


@pytest.fixture(scope="session")
def invalid_parameter_id():
    return "PAR-0000-0000"


@pytest.fixture
def created_parameter(mpt_ops, parameter_data):
    with create_fixture_resource_and_delete(
        mpt_ops.helpdesk.parameters, parameter_data
    ) as parameter:
        yield parameter


@pytest.fixture
async def async_created_parameter(async_mpt_ops, parameter_data):
    async with async_create_fixture_resource_and_delete(
        async_mpt_ops.helpdesk.parameters, parameter_data
    ) as parameter:
        yield parameter
