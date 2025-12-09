import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_subscription(mpt_vendor, subscription_factory):
    subscription_data = subscription_factory()

    subscription = mpt_vendor.commerce.subscriptions.create(subscription_data)

    yield subscription

    try:
        mpt_vendor.commerce.subscriptions.terminate(subscription.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to terminate subscription: {getattr(error, 'title', str(error))}")  # noqa: WPS421


def test_get_subscription_by_id(mpt_vendor, subscription_id):
    result = mpt_vendor.commerce.subscriptions.get(subscription_id)

    assert result is not None


def test_list_subscriptions(mpt_vendor):
    limit = 10

    result = mpt_vendor.commerce.subscriptions.fetch_page(limit=limit)

    assert result is not None


def test_get_subscription_by_id_not_found(mpt_vendor, invalid_subscription_id):
    with pytest.raises(MPTAPIError, match="404 Not Found"):
        mpt_vendor.commerce.subscriptions.get(invalid_subscription_id)


def test_filter_subscriptions(mpt_vendor, subscription_id):
    select_fields = ["-externalIds"]
    filtered_subscriptions = (
        mpt_vendor.commerce.subscriptions.filter(RQLQuery(id=subscription_id))
        .filter(RQLQuery(name="E2E Seeded Subscription"))
        .select(*select_fields)
    )

    result = list(filtered_subscriptions.iterate())

    assert len(result) == 1


def test_create_subscription(created_subscription):
    result = created_subscription

    assert result is not None


def test_update_subscription(mpt_vendor, created_subscription):
    updated_subscription_data = {
        "name": "E2E Updated Subscription",
    }

    result = mpt_vendor.commerce.subscriptions.update(
        created_subscription.id, updated_subscription_data
    )

    assert result is not None


def test_terminate_subscription(mpt_vendor, created_subscription):
    result = mpt_vendor.commerce.subscriptions.terminate(created_subscription.id)

    assert result is not None


def test_render_subscription(mpt_vendor, created_subscription):
    result = mpt_vendor.commerce.subscriptions.render(created_subscription.id)

    assert result is not None
