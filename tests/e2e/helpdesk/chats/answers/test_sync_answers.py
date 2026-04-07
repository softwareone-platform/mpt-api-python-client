from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.chat_answers import ChatAnswer

pytestmark = [pytest.mark.flaky]


def test_get_chat_answer(chat_answers_service, created_chat_answer):
    result = chat_answers_service.get(created_chat_answer.id)

    assert result.id == created_chat_answer.id


@pytest.mark.usefixtures("created_chat_answer")
def test_list_chat_answers(chat_answers_service):
    result = chat_answers_service.fetch_page(limit=1)

    assert len(result) > 0
    assert all(isinstance(answer, ChatAnswer) for answer in result)


def test_create_chat_answer(created_chat_answer):
    result = created_chat_answer

    assert isinstance(result, ChatAnswer)


def test_update_chat_answer(chat_answers_service, created_chat_answer, short_uuid):
    update_data = {"name": f"e2e updated answer {short_uuid}"}

    result = chat_answers_service.update(created_chat_answer.id, update_data)

    assert isinstance(result, ChatAnswer)
    assert result.to_dict().get("name") == update_data["name"]


def test_submit_chat_answer(chat_answers_service, created_chat_answer):
    result = chat_answers_service.submit(created_chat_answer.id)

    assert isinstance(result, ChatAnswer)


def test_query_chat_answer(chat_answers_service, created_chat_answer):
    submitted_chat_answer = chat_answers_service.submit(created_chat_answer.id)

    result = chat_answers_service.query(submitted_chat_answer.id)

    assert isinstance(result, ChatAnswer)


def test_validate_chat_answer(chat_answers_service, created_chat_answer):
    result = chat_answers_service.validate(created_chat_answer.id, {"parameters": []})

    assert isinstance(result, ChatAnswer)


def test_accept_chat_answer(chat_answers_service, submitted_chat_answer):
    result = chat_answers_service.accept(submitted_chat_answer.id)

    assert isinstance(result, ChatAnswer)


def test_delete_chat_answer(chat_answers_service, created_chat_answer):
    chat_answers_service.delete(created_chat_answer.id)  # act


def test_not_found(chat_answers_service, invalid_chat_answer_id):
    with pytest.raises(MPTAPIError) as error:
        chat_answers_service.get(invalid_chat_answer_id)

    assert error.value.status_code == HTTPStatus.NOT_FOUND
