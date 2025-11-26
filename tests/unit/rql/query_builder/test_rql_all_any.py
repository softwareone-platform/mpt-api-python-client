from mpt_api_client.rql import RQLQuery


def test_all():
    query = RQLQuery(saleDetails__orderQty__gt=1).all()

    result = str(query)

    assert result == "all(gt(saleDetails.orderQty,1))"


def test_any():
    query = RQLQuery(saleDetails__orderQty__gt=1).any()

    result = str(query)

    assert result == "any(gt(saleDetails.orderQty,1))"
