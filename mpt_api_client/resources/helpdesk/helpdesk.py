from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.helpdesk.cases import AsyncCasesService, CasesService
from mpt_api_client.resources.helpdesk.channels import AsyncChannelsService, ChannelsService
from mpt_api_client.resources.helpdesk.chats import AsyncChatsService, ChatsService
from mpt_api_client.resources.helpdesk.forms import AsyncFormsService, FormsService
from mpt_api_client.resources.helpdesk.parameter_groups import (
    AsyncParameterGroupsService,
    ParameterGroupsService,
)
from mpt_api_client.resources.helpdesk.parameters import (
    AsyncParametersService,
    ParametersService,
)
from mpt_api_client.resources.helpdesk.queues import AsyncQueuesService, QueuesService


class Helpdesk:
    """Helpdesk MPT API Module."""

    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def chats(self) -> ChatsService:
        """Chats service."""
        return ChatsService(http_client=self.http_client)

    @property
    def channels(self) -> ChannelsService:
        """Channels service."""
        return ChannelsService(http_client=self.http_client)

    @property
    def cases(self) -> CasesService:
        """Cases service."""
        return CasesService(http_client=self.http_client)

    @property
    def queues(self) -> QueuesService:
        """Queues service."""
        return QueuesService(http_client=self.http_client)

    @property
    def parameters(self) -> ParametersService:  # noqa: WPS110
        """Parameters service."""
        return ParametersService(http_client=self.http_client)

    @property
    def forms(self) -> FormsService:
        """Forms service."""
        return FormsService(http_client=self.http_client)

    @property
    def parameter_groups(self) -> ParameterGroupsService:
        """Parameter groups service."""
        return ParameterGroupsService(http_client=self.http_client)


class AsyncHelpdesk:
    """Async Helpdesk MPT API Module."""

    def __init__(self, http_client: AsyncHTTPClient):
        self.http_client = http_client

    @property
    def chats(self) -> AsyncChatsService:
        """Async Chats service."""
        return AsyncChatsService(http_client=self.http_client)

    @property
    def channels(self) -> AsyncChannelsService:
        """Async Channels service."""
        return AsyncChannelsService(http_client=self.http_client)

    @property
    def cases(self) -> AsyncCasesService:
        """Async Cases service."""
        return AsyncCasesService(http_client=self.http_client)

    @property
    def queues(self) -> AsyncQueuesService:
        """Async Queues service."""
        return AsyncQueuesService(http_client=self.http_client)

    @property
    def parameters(self) -> AsyncParametersService:  # noqa: WPS110
        """Async parameters service."""
        return AsyncParametersService(http_client=self.http_client)

    @property
    def forms(self) -> AsyncFormsService:
        """Async forms service."""
        return AsyncFormsService(http_client=self.http_client)

    @property
    def parameter_groups(self) -> AsyncParameterGroupsService:
        """Async parameter groups service."""
        return AsyncParameterGroupsService(http_client=self.http_client)
