import pytest

from mpt_api_client.resources.helpdesk import AsyncHelpdesk, Helpdesk
from mpt_api_client.resources.helpdesk.cases import AsyncCasesService, CasesService
from mpt_api_client.resources.helpdesk.channels import AsyncChannelsService, ChannelsService
from mpt_api_client.resources.helpdesk.chats import AsyncChatsService, ChatsService
from mpt_api_client.resources.helpdesk.parameter_groups import (
    AsyncParameterGroupsService,
    ParameterGroupsService,
)
from mpt_api_client.resources.helpdesk.parameters import (
    AsyncParametersService,
    ParametersService,
)
from mpt_api_client.resources.helpdesk.queues import AsyncQueuesService, QueuesService


def test_helpdesk_init(http_client):
    result = Helpdesk(http_client=http_client)

    assert isinstance(result, Helpdesk)
    assert result.http_client is http_client


def test_async_helpdesk_init(async_http_client):
    result = AsyncHelpdesk(http_client=async_http_client)

    assert isinstance(result, AsyncHelpdesk)
    assert result.http_client is async_http_client


@pytest.mark.parametrize(
    ("attr_name", "expected"),
    [
        ("chats", ChatsService),
        ("channels", ChannelsService),
        ("cases", CasesService),
        ("queues", QueuesService),
        ("parameters", ParametersService),
        ("parameter_groups", ParameterGroupsService),
    ],
)
def test_helpdesk_properties(http_client, attr_name, expected):
    helpdesk = Helpdesk(http_client=http_client)

    result = getattr(helpdesk, attr_name)

    assert isinstance(result, expected)


@pytest.mark.parametrize(
    ("attr_name", "expected"),
    [
        ("chats", AsyncChatsService),
        ("channels", AsyncChannelsService),
        ("cases", AsyncCasesService),
        ("queues", AsyncQueuesService),
        ("parameters", AsyncParametersService),
        ("parameter_groups", AsyncParameterGroupsService),
    ],
)
def test_async_helpdesk_properties(async_http_client, attr_name, expected):
    helpdesk = AsyncHelpdesk(http_client=async_http_client)

    result = getattr(helpdesk, attr_name)

    assert isinstance(result, expected)
