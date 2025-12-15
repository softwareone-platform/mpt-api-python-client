import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


async def test_get_subscriber_by_id(async_mpt_client, subscriber_id):
    result = await async_mpt_client.notifications.subscribers.get(subscriber_id)

    assert result is not None


async def test_list_subscribers(async_mpt_client):
    limit = 10

    result = await async_mpt_client.notifications.subscribers.fetch_page(limit=limit)

    assert len(result) > 0


async def test_get_subscriber_by_id_not_found(async_mpt_client, invalid_subscriber_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_client.notifications.subscribers.get(invalid_subscriber_id)


async def test_filter_subscribers(async_mpt_client, subscriber_id):
    select_fields = ["-config"]
    async_filtered_subscribers = async_mpt_client.notifications.subscribers.filter(
        RQLQuery(id=subscriber_id)
    ).select(*select_fields)

    result = [
        filtered_subscriber async for filtered_subscriber in async_filtered_subscribers.iterate()
    ]

    assert len(result) > 0


async def test_update_subscriber_not_found(
    async_mpt_client, subscriber_factory, invalid_subscriber_id, recipients_factory
):
    updated_subscriber_data = subscriber_factory(recipients=recipients_factory())

    with pytest.raises(MPTAPIError):
        await async_mpt_client.notifications.subscribers.update(
            invalid_subscriber_id, updated_subscriber_data
        )


async def test_disable_subscriber(async_mpt_client, active_subscriber_id):
    result = await async_mpt_client.notifications.subscribers.disable(active_subscriber_id)

    assert result is not None
    assert result.status == "Disabled"


async def test_disable_subscriber_not_found(async_mpt_client, invalid_subscriber_id):
    with pytest.raises(
        MPTAPIError, match=r"400 Bad Request - Subscriber with id 'NTS-0000-0000-0000' not found"
    ):
        await async_mpt_client.notifications.subscribers.disable(invalid_subscriber_id)


async def test_enable_subscriber(async_mpt_client, disabled_subscriber_id):
    result = await async_mpt_client.notifications.subscribers.enable(disabled_subscriber_id)

    assert result is not None
    assert result.status == "Active"


async def test_enable_subscriber_not_found(async_mpt_client, invalid_subscriber_id):
    with pytest.raises(
        MPTAPIError, match=r"400 Bad Request - Subscriber with id 'NTS-0000-0000-0000' not found"
    ):
        await async_mpt_client.notifications.subscribers.enable(invalid_subscriber_id)
