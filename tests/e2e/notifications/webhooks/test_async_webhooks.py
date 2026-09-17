import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import (
    assert_async_service_filter_with_iterate,
    assert_async_update_resource,
)

pytestmark = [pytest.mark.flaky]


def test_create_webhook(async_created_webhook, webhook_data):
    result = async_created_webhook.url

    assert result == webhook_data["url"]


async def test_get_webhook(async_webhooks_service, async_created_webhook):
    result = await async_webhooks_service.get(async_created_webhook.id)

    assert result.id == async_created_webhook.id


async def test_get_webhook_not_found(async_webhooks_service):
    bogus_id = "WBH-0000-0000"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_webhooks_service.get(bogus_id)


async def test_update_webhook(async_webhooks_service, async_created_webhook, short_uuid):
    new_description = f"e2e webhook updated {short_uuid}"

    await assert_async_update_resource(  # act
        async_webhooks_service, async_created_webhook.id, "description", new_description
    )


async def test_disable_webhook(async_webhooks_service, async_created_webhook):
    result = await async_webhooks_service.disable(async_created_webhook.id)

    assert result.status == "Disabled"


async def test_enable_webhook(async_webhooks_service, async_created_webhook):
    await async_webhooks_service.disable(async_created_webhook.id)

    result = await async_webhooks_service.enable(async_created_webhook.id)

    assert result.status == "Enabled"


async def test_delete_webhook(async_webhooks_service, async_created_webhook):
    await async_webhooks_service.delete(async_created_webhook.id)  # act


async def test_delete_webhook_not_found(async_webhooks_service):
    bogus_id = "WBH-0000-0000"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_webhooks_service.delete(bogus_id)


async def test_filter_webhooks(async_webhooks_service, async_created_webhook):
    await assert_async_service_filter_with_iterate(  # act
        async_webhooks_service, async_created_webhook.id, None
    )
