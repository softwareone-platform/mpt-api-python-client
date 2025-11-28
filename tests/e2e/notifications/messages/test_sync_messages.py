import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


def test_get_message(mpt_client, message_id):
    service = mpt_client.notifications.messages

    result = service.get(message_id)

    assert result.id == message_id


def test_list_messages(mpt_ops):
    service = mpt_ops.notifications.messages

    result = service.fetch_page(limit=1)

    assert len(result) > 0


def test_not_found(mpt_client, invalid_message_id):
    service = mpt_client.notifications.messages

    with pytest.raises(MPTAPIError):
        service.get(invalid_message_id)
