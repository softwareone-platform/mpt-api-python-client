from mpt_api_client.rql import RQLQuery


def test_all():
    query = RQLQuery(orderQty__gt=1).all("saleDetails")

    result = str(query)

    assert result == "all(saleDetails,gt(orderQty,'1'))"


def test_any():
    query = RQLQuery(orderQty__gt=1).any("saleDetails")

    result = str(query)

    assert result == "any(saleDetails,gt(orderQty,'1'))"


def test_all_multiple_conditions():
    order_qty_query = RQLQuery(orderQty__gt=1)
    price_query = RQLQuery(price__lt=100)
    query = (order_qty_query & price_query).all("saleDetails")

    result = str(query)

    assert result == "all(saleDetails,and(gt(orderQty,'1'),lt(price,'100')))"


def test_any_multiple_conditions():
    order_qty_query = RQLQuery(orderQty__gt=1)
    price_query = RQLQuery(price__lt=100)
    query = (order_qty_query & price_query).any("saleDetails")

    result = str(query)

    assert result == "any(saleDetails,and(gt(orderQty,'1'),lt(price,'100')))"
