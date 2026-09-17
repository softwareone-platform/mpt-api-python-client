from http import HTTPStatus

import pytest

from tests.e2e.helper import (
    async_create_first_free_fixture_and_delete,
    create_first_free_fixture_and_delete,
)

# The platform allows one webhook per type and bound object. The create call is the claim on
# a type: a run tries these order-validation types in order and moves on when the platform
# answers 409 Conflict, so concurrent runs sharing the seeded product cannot both win the
# same type.
WEBHOOK_TYPES = (
    "ValidatePurchaseOrderDraft",
    "ValidateChangeOrderDraft",
    "ValidateTerminateOrder",
    "ValidatePurchaseOrderQuerying",
    "ValidateConfigurationOrderDraft",
)


def _is_type_taken(error):
    return error.status_code == HTTPStatus.CONFLICT


@pytest.fixture
def webhooks_service(mpt_vendor):
    return mpt_vendor.notifications.webhooks


@pytest.fixture
def async_webhooks_service(async_mpt_vendor):
    return async_mpt_vendor.notifications.webhooks


@pytest.fixture
def webhook_data(product_id, short_uuid, uuid_str):
    return {
        "url": f"https://example.com/e2e/{short_uuid}",
        "description": f"e2e webhook - please delete {short_uuid}",
        "criteria": {"product.id": product_id},
        "secret": f"e2e-webhook-secret-{uuid_str}",
    }


@pytest.fixture
def webhook_candidates(webhook_data):
    return [{**webhook_data, "type": webhook_type} for webhook_type in WEBHOOK_TYPES]


@pytest.fixture
def created_webhook(webhooks_service, webhook_candidates):
    with create_first_free_fixture_and_delete(
        webhooks_service, webhook_candidates, _is_type_taken
    ) as webhook:
        yield webhook


@pytest.fixture
async def async_created_webhook(async_webhooks_service, webhook_candidates):
    async with async_create_first_free_fixture_and_delete(
        async_webhooks_service, webhook_candidates, _is_type_taken
    ) as webhook:
        yield webhook
