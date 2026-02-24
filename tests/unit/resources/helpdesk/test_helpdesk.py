import pytest

from mpt_api_client.resources import AsyncHelpdesk, Helpdesk
from mpt_api_client.resources.helpdesk.cases import AsyncCasesService, CasesService


@pytest.fixture
def helpdesk(http_client):
    return Helpdesk(http_client=http_client)


@pytest.fixture
def async_helpdesk(async_http_client):
    return AsyncHelpdesk(http_client=async_http_client)


@pytest.mark.parametrize(
    ("attr_name", "expected"),
    [
        ("cases", CasesService),
    ],
)
def test_helpdesk_properties(helpdesk, attr_name, expected):
    result = getattr(helpdesk, attr_name)

    assert isinstance(result, expected)


@pytest.mark.parametrize(
    ("attr_name", "expected"),
    [
        ("cases", AsyncCasesService),
    ],
)
def test_async_helpdesk_properties(async_helpdesk, attr_name, expected):
    result = getattr(async_helpdesk, attr_name)

    assert isinstance(result, expected)
