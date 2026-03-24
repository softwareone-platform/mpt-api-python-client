import pytest

from mpt_api_client.resources.helpdesk.chat_answer_parameters import (
    AsyncChatAnswerParametersService,
    ChatAnswerParametersService,
)


@pytest.fixture
def chat_answer_parameters_service(http_client) -> ChatAnswerParametersService:
    return ChatAnswerParametersService(
        http_client=http_client,
        endpoint_params={"chat_id": "CHT-0000-0000-0001", "answer_id": "ANS-0000-0000"},
    )


@pytest.fixture
def async_chat_answer_parameters_service(async_http_client) -> AsyncChatAnswerParametersService:
    return AsyncChatAnswerParametersService(
        http_client=async_http_client,
        endpoint_params={"chat_id": "CHT-0000-0000-0001", "answer_id": "ANS-0000-0000"},
    )


def test_endpoint(chat_answer_parameters_service) -> None:
    result = (
        chat_answer_parameters_service.path
        == "/public/v1/helpdesk/chats/CHT-0000-0000-0001/answers/ANS-0000-0000/parameters"
    )

    assert result is True


def test_async_endpoint(async_chat_answer_parameters_service) -> None:
    result = (
        async_chat_answer_parameters_service.path
        == "/public/v1/helpdesk/chats/CHT-0000-0000-0001/answers/ANS-0000-0000/parameters"
    )

    assert result is True


@pytest.mark.parametrize("method", ["fetch_page", "iterate"])
def test_methods_present(chat_answer_parameters_service, method: str) -> None:
    result = hasattr(chat_answer_parameters_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete"])
def test_methods_absent(chat_answer_parameters_service, method: str) -> None:
    result = hasattr(chat_answer_parameters_service, method)

    assert result is False


@pytest.mark.parametrize("method", ["fetch_page", "iterate"])
def test_async_methods_present(async_chat_answer_parameters_service, method: str) -> None:
    result = hasattr(async_chat_answer_parameters_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete"])
def test_async_methods_absent(async_chat_answer_parameters_service, method: str) -> None:
    result = hasattr(async_chat_answer_parameters_service, method)

    assert result is False
