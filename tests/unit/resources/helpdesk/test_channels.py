import pytest

from mpt_api_client.resources.helpdesk.channel_messages import (
    AsyncChannelMessagesService,
    ChannelMessagesService,
)
from mpt_api_client.resources.helpdesk.channels import AsyncChannelsService, ChannelsService


@pytest.fixture
def channels_service(http_client):
    return ChannelsService(http_client=http_client)


@pytest.fixture
def async_channels_service(async_http_client):
    return AsyncChannelsService(http_client=async_http_client)


def test_endpoint(channels_service) -> None:
    result = channels_service.path == "/public/v1/helpdesk/channels"

    assert result is True


def test_async_endpoint(async_channels_service) -> None:
    result = async_channels_service.path == "/public/v1/helpdesk/channels"

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "fetch_page", "iterate", "messages"],
)
def test_methods_present(channels_service, method):
    result = hasattr(channels_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "fetch_page", "iterate", "messages"],
)
def test_async_methods_present(async_channels_service, method):
    result = hasattr(async_channels_service, method)

    assert result is True


def test_messages_service(channels_service):
    result = channels_service.messages("CHN-0000-0000-0001")

    assert isinstance(result, ChannelMessagesService)
    assert result.endpoint_params == {"channel_id": "CHN-0000-0000-0001"}


def test_async_messages_service(async_channels_service):
    result = async_channels_service.messages("CHN-0000-0000-0001")

    assert isinstance(result, AsyncChannelMessagesService)
    assert result.endpoint_params == {"channel_id": "CHN-0000-0000-0001"}
