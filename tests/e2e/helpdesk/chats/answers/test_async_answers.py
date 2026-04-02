from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.chat_answers import ChatAnswer

pytestmark = [
    pytest.mark.flaky,
    pytest.mark.skip(reason="Unskip after MPT-19124 completed"),
]


async def test_get_chat_answer(async_chat_answers_service, async_created_chat_answer):
    result = await async_chat_answers_service.get(async_created_chat_answer.id)

    assert isinstance(result, ChatAnswer)


async def test_list_chat_answers(async_chat_answers_service):
    result = await async_chat_answers_service.fetch_page(limit=1)

    assert len(result) > 0
    assert all(isinstance(answer, ChatAnswer) for answer in result)


def test_create_chat_answer(async_created_chat_answer):
    result = async_created_chat_answer

    assert isinstance(result, ChatAnswer)


async def test_update_chat_answer(
    async_chat_answers_service, async_created_chat_answer, short_uuid
):
    update_data = {"name": f"e2e updated answer {short_uuid}"}

    result = await async_chat_answers_service.update(async_created_chat_answer.id, update_data)

    assert isinstance(result, ChatAnswer)
    assert result.to_dict().get("name") == update_data["name"]


async def test_submit_chat_answer(async_chat_answers_service, async_created_chat_answer):
    result = await async_chat_answers_service.submit(async_created_chat_answer.id)

    assert isinstance(result, ChatAnswer)


async def test_query_chat_answer(async_chat_answers_service, async_created_chat_answer):
    submitted_chat_answer = await async_chat_answers_service.submit(async_created_chat_answer.id)

    result = await async_chat_answers_service.query(submitted_chat_answer.id)

    assert isinstance(result, ChatAnswer)


async def test_validate_chat_answer(async_chat_answers_service, async_created_chat_answer):
    result = await async_chat_answers_service.validate(
        async_created_chat_answer.id,
        {"parameters": []},
    )

    assert isinstance(result, ChatAnswer)


async def test_accept_chat_answer(async_chat_answers_service, async_created_chat_answer):
    result = await async_chat_answers_service.accept(async_created_chat_answer.id)

    assert isinstance(result, ChatAnswer)


async def test_delete_chat_answer(async_chat_answers_service, async_created_chat_answer):
    await async_chat_answers_service.delete(async_created_chat_answer.id)  # act


async def test_not_found(async_chat_answers_service, invalid_chat_answer_id):
    with pytest.raises(MPTAPIError) as error:
        await async_chat_answers_service.get(invalid_chat_answer_id)
    assert error.value.status_code == HTTPStatus.NOT_FOUND
