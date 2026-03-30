import pytest


@pytest.fixture(scope="session")
def invalid_case_id():
    return "CAS-0000-0000"


@pytest.fixture
def case_factory(short_uuid):
    def factory(
        title: str = "E2E Created Helpdesk Case",
        description: str = "E2E Created Helpdesk Case Description",
    ):
        return {
            "title": f"{title} {short_uuid}",
            "description": description,
            "priority": "Low",
            "type": "General",
        }

    return factory


@pytest.fixture
def created_case(mpt_ops, case_factory):
    return mpt_ops.helpdesk.cases.create(case_factory())


@pytest.fixture
async def async_created_case(async_mpt_ops, case_factory):
    return await async_mpt_ops.helpdesk.cases.create(case_factory())
