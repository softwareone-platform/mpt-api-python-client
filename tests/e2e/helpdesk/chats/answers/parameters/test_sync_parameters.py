from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.chat_answer_parameters import ChatAnswerParameter

pytestmark = [
    pytest.mark.flaky,
    pytest.mark.skip(reason="Unskip after MPT-19124 completed"),
]


def test_list_chat_answer_parameters(chat_answer_parameters_service):
    result = chat_answer_parameters_service.fetch_page(limit=20)

    assert len(result) > 0
    assert all(isinstance(parameter, ChatAnswerParameter) for parameter in result)


def test_iterate_chat_answer_parameters(chat_answer_parameters_service):
    iterator = chat_answer_parameters_service.iterate(limit=20)

    result = next(iterator, None)

    assert result is None or result.id is not None


def test_not_found(mpt_ops, chat_id):
    service = mpt_ops.helpdesk.chats.answers(chat_id).parameters("ANS-0000-0000")

    with pytest.raises(MPTAPIError) as error:
        service.fetch_page(limit=20)

    assert error.value.status_code == HTTPStatus.NOT_FOUND
