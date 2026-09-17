import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import assert_service_filter_with_iterate, assert_update_resource

pytestmark = [pytest.mark.flaky]


def test_create_webhook(created_webhook, webhook_data):
    result = created_webhook.url

    assert result == webhook_data["url"]


def test_get_webhook(webhooks_service, created_webhook):
    result = webhooks_service.get(created_webhook.id)

    assert result.id == created_webhook.id


def test_get_webhook_not_found(webhooks_service):
    bogus_id = "WBH-0000-0000"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        webhooks_service.get(bogus_id)


def test_update_webhook(webhooks_service, created_webhook, short_uuid):
    new_description = f"e2e webhook updated {short_uuid}"

    assert_update_resource(  # act
        webhooks_service, created_webhook.id, "description", new_description
    )


def test_disable_webhook(webhooks_service, created_webhook):
    result = webhooks_service.disable(created_webhook.id)

    assert result.status == "Disabled"


def test_enable_webhook(webhooks_service, created_webhook):
    webhooks_service.disable(created_webhook.id)

    result = webhooks_service.enable(created_webhook.id)

    assert result.status == "Enabled"


def test_delete_webhook(webhooks_service, created_webhook):
    webhooks_service.delete(created_webhook.id)  # act


def test_delete_webhook_not_found(webhooks_service):
    bogus_id = "WBH-0000-0000"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        webhooks_service.delete(bogus_id)


def test_filter_webhooks(webhooks_service, created_webhook):
    assert_service_filter_with_iterate(webhooks_service, created_webhook.id, None)  # act
