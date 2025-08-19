
from mpt_api_client.modules.order import Order, OrderCollectionClient


def test_order_collection_client(mpt_client):
    order_cc = OrderCollectionClient(client=mpt_client)
    assert order_cc.query_rql is None


def test_order():
    order = Order()
    assert order is not None
