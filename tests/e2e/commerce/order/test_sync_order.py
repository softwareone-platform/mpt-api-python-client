import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_order(mpt_client, order_factory):
    new_order_request_data = order_factory()

    return mpt_client.commerce.orders.create(new_order_request_data)


@pytest.fixture
def processed_order(mpt_client, created_order):
    return mpt_client.commerce.orders.process(created_order.id)


def test_get_order_by_id(mpt_client, order_id):
    result = mpt_client.commerce.orders.get(order_id)

    assert result is not None


def test_list_orders(mpt_client):
    limit = 10

    result = mpt_client.commerce.orders.fetch_page(limit=limit)

    assert len(result) > 0


def test_get_order_by_id_not_found(mpt_client, invalid_order_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_client.commerce.orders.get(invalid_order_id)


def test_filter_orders(mpt_client, order_id):
    select_fields = ["-authorization"]
    filtered_orders = (
        mpt_client.commerce.orders
        .filter(RQLQuery(id=order_id))
        .filter(RQLQuery(type="Purchase"))
        .select(*select_fields)
    )

    result = list(filtered_orders.iterate())

    assert len(result) == 1


def test_create_order(created_order):
    result = created_order

    assert result is not None


def test_update_order(mpt_client, created_order, order_factory):
    update_data = order_factory(notes="E2E Updated Order Notes")

    result = mpt_client.commerce.orders.update(created_order.id, update_data)

    assert result is not None


def test_process_order(mpt_client, created_order):
    result = mpt_client.commerce.orders.process(created_order.id)

    assert result is not None


def test_query_order(mpt_vendor, mpt_client, created_order):
    processed_order = mpt_client.commerce.orders.process(created_order.id)

    result = mpt_vendor.commerce.orders.query(processed_order.id)

    assert result is not None


def test_complete_order(mpt_vendor, order_subscription_factory, processed_order):
    processed_order_lines = processed_order.lines
    line_id = processed_order_lines[0].id
    order_subscription = order_subscription_factory(line_id)
    order_subscriptions = mpt_vendor.commerce.orders.subscriptions(processed_order.id)
    order_subscriptions.create(order_subscription)

    result = mpt_vendor.commerce.orders.complete(processed_order.id)

    assert result is not None


def test_fail_order(mpt_vendor, processed_order):
    fail_order_data = {
        "statusNotes": {
            "message": "Failing order for E2E test",
            "id": processed_order.id,
        }
    }

    result = mpt_vendor.commerce.orders.fail(processed_order.id, fail_order_data)

    assert result is not None


def test_delete_draft_order(mpt_client, created_order):
    result = created_order

    mpt_client.commerce.orders.delete(result.id)


def test_quote_order(mpt_client, created_order):
    result = mpt_client.commerce.orders.quote(created_order.id)

    assert result is not None


def test_validate_order(mpt_client, created_order):
    result = mpt_client.commerce.orders.validate(created_order.id)

    assert result is not None


def test_order_template(mpt_client, created_order):
    result = mpt_client.commerce.orders.template(created_order.id)

    assert result is not None


def test_order_render(mpt_client, created_order):
    result = mpt_client.commerce.orders.render(created_order.id)

    assert result is not None


def test_notify_order(mpt_client, created_order, commerce_user_id):
    user_data = {
        "userId": commerce_user_id,
        "notifyMe": False,
    }

    result = mpt_client.commerce.orders.quote(created_order.id)

    mpt_client.commerce.orders.notify(result.id, user_data)
