import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


def test_get_message(mpt_client, message_id):
    if message_id is None:
        pytest.skip("Message ID not configured in e2e_config")

    service = mpt_client.notifications.messages

    result = service.get(message_id)

    assert result.id == message_id


def test_list_messages(mpt_client):
    service = mpt_client.notifications.messages

    result = service.fetch_page(limit=10)

    assert len(result) > 0


def test_not_found(mpt_client):
    service = mpt_client.notifications.messages

    with pytest.raises(MPTAPIError):
        service.get("MSG-000-000-000")
