from mpt_api_client.rql import Property, RQLQuery, Value


def test_compare_default_value():
    query = RQLQuery(agreement__product__id="order.product.id")

    result = str(query)

    assert result == "eq(agreement.product.id,'order.product.id')"


def test_compare_quoted():
    query = RQLQuery(agreement__product__id=Value("order.product.id"))

    result = str(query)

    assert result == "eq(agreement.product.id,'order.product.id')"


def test_compare_property():
    query = RQLQuery(agreement__product__id=Property("order.product.id"))

    result = str(query)

    assert result == "eq(agreement.product.id,order.product.id)"


def test_ne_quoted():
    query = RQLQuery("agreement.product.id")

    result = str(query.ne(Value("order.product.id")))

    assert result == "ne(agreement.product.id,'order.product.id')"


def test_ne_property():
    query = RQLQuery("agreement.product.id")

    result = str(query.ne(Property("order.product.id")))

    assert result == "ne(agreement.product.id,order.product.id)"
