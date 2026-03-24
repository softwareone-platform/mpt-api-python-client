import pytest

from mpt_api_client.resources.helpdesk.channel_messages import (
    AsyncChannelMessagesService,
    ChannelMessagesService,
)


@pytest.fixture
def channel_messages_service(http_client) -> ChannelMessagesService:
    return ChannelMessagesService(
        http_client=http_client, endpoint_params={"channel_id": "CHN-0000-0000-0001"}
    )


@pytest.fixture
def async_channel_messages_service(async_http_client) -> AsyncChannelMessagesService:
    return AsyncChannelMessagesService(
        http_client=async_http_client,
        endpoint_params={"channel_id": "CHN-0000-0000-0001"},
    )


def test_endpoint(channel_messages_service) -> None:
    result = (
        channel_messages_service.path == "/public/v1/helpdesk/channels/CHN-0000-0000-0001/messages"
    )

    assert result is True


def test_async_endpoint(async_channel_messages_service) -> None:
    result = (
        async_channel_messages_service.path
        == "/public/v1/helpdesk/channels/CHN-0000-0000-0001/messages"
    )

    assert result is True


@pytest.mark.parametrize("method", ["fetch_page", "iterate"])
def test_methods_present(channel_messages_service, method: str) -> None:
    result = hasattr(channel_messages_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete"])
def test_methods_absent(channel_messages_service, method: str) -> None:
    result = hasattr(channel_messages_service, method)

    assert result is False


@pytest.mark.parametrize("method", ["fetch_page", "iterate"])
def test_async_methods_present(async_channel_messages_service, method: str) -> None:
    result = hasattr(async_channel_messages_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete"])
def test_async_methods_absent(async_channel_messages_service, method: str) -> None:
    result = hasattr(async_channel_messages_service, method)

    assert result is False
