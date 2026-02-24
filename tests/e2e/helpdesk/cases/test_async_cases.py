import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_case(async_mpt_ops, case_data):
    service = async_mpt_ops.helpdesk.cases
    try:
        return await service.create(case_data)
    except MPTAPIError as error:
        pytest.skip(f"Support case create is not available in this environment: {error.title}")


def test_create_case(created_case):
    result = created_case.id

    assert result is not None


async def test_get_case(async_mpt_ops, created_case):
    service = async_mpt_ops.helpdesk.cases

    result = await service.get(created_case.id)

    assert result.id == created_case.id


async def test_update_case(
    async_mpt_ops,
    created_case,
    case_update_data,
):
    service = async_mpt_ops.helpdesk.cases

    result = await service.update(created_case.id, case_update_data)

    assert result.id == created_case.id


async def test_list_cases(async_mpt_ops):
    service = async_mpt_ops.helpdesk.cases

    result = await service.fetch_page(limit=1)

    assert result is not None
