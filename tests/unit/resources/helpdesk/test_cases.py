import pytest

from mpt_api_client.resources.helpdesk.cases import AsyncCasesService, CasesService


@pytest.fixture
def cases_service(http_client):
    return CasesService(http_client=http_client)


@pytest.fixture
def async_cases_service(async_http_client):
    return AsyncCasesService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method", ["complete", "create", "get", "iterate", "process", "query", "update"]
)
def test_mixins_present(cases_service, method):
    result = hasattr(cases_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method", ["complete", "create", "get", "iterate", "process", "query", "update"]
)
def test_async_mixins_present(async_cases_service, method):
    result = hasattr(async_cases_service, method)

    assert result is True


def test_endpoint(cases_service):
    result = cases_service.path == "/public/v1/helpdesk/cases"

    assert result is True


def test_async_endpoint(async_cases_service):
    result = async_cases_service.path == "/public/v1/helpdesk/cases"

    assert result is True
