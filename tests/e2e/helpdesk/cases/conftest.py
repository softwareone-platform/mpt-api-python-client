import pytest


@pytest.fixture(scope="session")
def invalid_case_id():
    return "CAS-0000-0000"


@pytest.fixture
def case_factory(short_uuid, created_queue):
    def factory(
        title: str = "E2E Created Helpdesk Case",
        description: str = "E2E Created Helpdesk Case Description",
    ):
        return {
            "queue": {"id": created_queue.id},
            "chat": {"lastMessage": {"content": "E2E testing!!!"}},
        }

    return factory


@pytest.fixture
def created_case(mpt_ops, case_factory):
    return mpt_ops.helpdesk.cases.create(case_factory())


@pytest.fixture
def queried_case(mpt_ops, created_case):
    return mpt_ops.helpdesk.cases.query(created_case.id, {"queryPrompt": "More details needed"})


@pytest.fixture
def processed_case(mpt_ops, queried_case):
    return mpt_ops.helpdesk.cases.process(queried_case.id)


@pytest.fixture
async def async_created_case(async_mpt_ops, case_factory):
    return await async_mpt_ops.helpdesk.cases.create(case_factory())


@pytest.fixture
async def async_queried_case(async_mpt_ops, async_created_case):
    return await async_mpt_ops.helpdesk.cases.query(
        async_created_case.id, {"queryPrompt": "More details needed"}
    )


@pytest.fixture
async def async_processed_case(async_mpt_ops, async_queried_case):
    return await async_mpt_ops.helpdesk.cases.process(async_queried_case.id)
