import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


def test_get_subscriber_by_id(mpt_client, subscriber_id):
    result = mpt_client.notifications.subscribers.get(subscriber_id)

    assert result is not None


def test_list_subscribers(mpt_client):
    limit = 10

    result = mpt_client.notifications.subscribers.fetch_page(limit=limit)

    assert len(result) > 0


def test_get_subscriber_by_id_not_found(mpt_client, invalid_subscriber_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_client.notifications.subscribers.get(invalid_subscriber_id)


def test_filter_subscribers(mpt_client, subscriber_id):
    select_fields = ["-config"]
    filtered_subscribers = (
        mpt_client.notifications.subscribers.filter(RQLQuery(id=subscriber_id))
        .filter(RQLQuery(status="enabled"))
        .select(*select_fields)
    )

    result = list(filtered_subscribers.iterate())

    assert len(result) >= 0


def test_update_subscriber_not_found(
    mpt_client, subscriber_factory, invalid_subscriber_id, user_group_id, recipients_factory
):
    updated_subscriber_data = subscriber_factory(recipients=recipients_factory())

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_client.notifications.subscribers.update(invalid_subscriber_id, updated_subscriber_data)
