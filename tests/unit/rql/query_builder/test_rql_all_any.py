from mpt_api_client.rql import RQLQuery


def test_all():
    query = RQLQuery(saleDetails__orderQty__gt=1).all()

    rql = str(query)
    assert rql == "all(gt(saleDetails.orderQty,1))"


def test_any():
    query = RQLQuery(saleDetails__orderQty__gt=1).any()
    rql = str(query)
    assert rql == "any(gt(saleDetails.orderQty,1))"
