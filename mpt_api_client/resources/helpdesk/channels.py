from mpt_api_client.http import AsyncService, Service, mixins
from mpt_api_client.models import Model
from mpt_api_client.resources.helpdesk.channel_messages import (
    AsyncChannelMessagesService,
    ChannelMessagesService,
)


class Channel(Model):
    """Helpdesk Channel resource."""


class ChannelsServiceConfig:
    """Helpdesk Channels service configuration."""

    _endpoint = "/public/v1/helpdesk/channels"
    _model_class = Channel
    _collection_key = "data"


class ChannelsService(
    mixins.CreateMixin[Channel],
    mixins.UpdateMixin[Channel],
    mixins.GetMixin[Channel],
    mixins.DeleteMixin,
    mixins.CollectionMixin[Channel],
    Service[Channel],
    ChannelsServiceConfig,
):
    """Helpdesk Channels service."""

    def messages(self, channel_id: str) -> ChannelMessagesService:
        """Return channel messages service."""
        return ChannelMessagesService(
            http_client=self.http_client,
            endpoint_params={"channel_id": channel_id},
        )


class AsyncChannelsService(
    mixins.AsyncCreateMixin[Channel],
    mixins.AsyncUpdateMixin[Channel],
    mixins.AsyncGetMixin[Channel],
    mixins.AsyncDeleteMixin,
    mixins.AsyncCollectionMixin[Channel],
    AsyncService[Channel],
    ChannelsServiceConfig,
):
    """Async Helpdesk Channels service."""

    def messages(self, channel_id: str) -> AsyncChannelMessagesService:
        """Return async channel messages service."""
        return AsyncChannelMessagesService(
            http_client=self.http_client,
            endpoint_params={"channel_id": channel_id},
        )
