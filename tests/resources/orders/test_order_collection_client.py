from mpt_api_client.resources.order import OrderCollectionClientBase


def test_order_collection_client(mpt_client):
    order_cc = OrderCollectionClientBase(http_client=mpt_client)
    assert order_cc.query_rql is None
