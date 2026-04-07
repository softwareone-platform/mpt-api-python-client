import httpx
import pytest
import respx

from mpt_api_client.resources.helpdesk.chat_answers import (
    AsyncChatAnswersService,
    ChatAnswer,
    ChatAnswersService,
)


@pytest.fixture
def chat_answers_service(http_client) -> ChatAnswersService:
    return ChatAnswersService(
        http_client=http_client, endpoint_params={"chat_id": "CHT-0000-0000-0001"}
    )


@pytest.fixture
def async_chat_answers_service(async_http_client) -> AsyncChatAnswersService:
    return AsyncChatAnswersService(
        http_client=async_http_client,
        endpoint_params={"chat_id": "CHT-0000-0000-0001"},
    )


def test_endpoint(chat_answers_service) -> None:
    result = chat_answers_service.path == "/public/v1/helpdesk/chats/CHT-0000-0000-0001/answers"

    assert result is True


def test_async_endpoint(async_chat_answers_service) -> None:
    result = (
        async_chat_answers_service.path == "/public/v1/helpdesk/chats/CHT-0000-0000-0001/answers"
    )

    assert result is True


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "create",
        "update",
        "delete",
        "fetch_page",
        "iterate",
        "submit",
        "accept",
        "query",
        "validate",
    ],
)
def test_methods_present(chat_answers_service, method: str) -> None:
    result = hasattr(chat_answers_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "create",
        "update",
        "delete",
        "fetch_page",
        "iterate",
        "submit",
        "accept",
        "query",
        "validate",
    ],
)
def test_async_methods_present(async_chat_answers_service, method: str) -> None:
    result = hasattr(async_chat_answers_service, method)

    assert result is True


@pytest.mark.parametrize("action", ["submit", "accept", "query", "validate"])
def test_custom_resource_actions(chat_answers_service, action):
    response_expected_data = {"id": "ANS-1234-5678", "status": "Updated"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/helpdesk/chats/CHT-0000-0000-0001/answers/ANS-1234-5678/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(chat_answers_service, action)("ANS-1234-5678")

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == b""
        assert result.to_dict() == response_expected_data
        assert isinstance(result, ChatAnswer)


@pytest.mark.parametrize("action", ["submit", "accept", "query", "validate"])
async def test_async_custom_resource_actions(async_chat_answers_service, action):
    response_expected_data = {"id": "ANS-1234-5678", "status": "Updated"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/helpdesk/chats/CHT-0000-0000-0001/answers/ANS-1234-5678/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_chat_answers_service, action)("ANS-1234-5678")

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == b""
        assert result.to_dict() == response_expected_data
        assert isinstance(result, ChatAnswer)
