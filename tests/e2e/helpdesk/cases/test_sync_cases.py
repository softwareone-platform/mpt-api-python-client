import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_case(mpt_ops, case_data):
    service = mpt_ops.helpdesk.cases
    try:
        return service.create(case_data)
    except MPTAPIError as error:
        pytest.skip(f"Support case create is not available in this environment: {error.title}")


def test_create_case(created_case):
    result = created_case.id

    assert result is not None


def test_get_case(mpt_ops, created_case):
    service = mpt_ops.helpdesk.cases

    result = service.get(created_case.id)

    assert result.id == created_case.id


def test_update_case(mpt_ops, created_case, case_update_data):
    service = mpt_ops.helpdesk.cases

    result = service.update(created_case.id, case_update_data)

    assert result.id == created_case.id


def test_list_cases(mpt_ops):
    service = mpt_ops.helpdesk.cases

    result = service.fetch_page(limit=1)

    assert result is not None
