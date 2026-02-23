from mpt_api_client.rql import RQLProperty, RQLQuery, RQLValue


def test_compare_default_value():
    query = RQLQuery(agreement__product__id="order.product.id")

    result = str(query)

    assert result == "eq(agreement.product.id,'order.product.id')"


def test_compare_quoted():
    query = RQLQuery(agreement__product__id=RQLValue("order.product.id"))

    result = str(query)

    assert result == "eq(agreement.product.id,'order.product.id')"


def test_compare_property():
    query = RQLQuery(agreement__product__id=RQLProperty("order.product.id"))

    result = str(query)

    assert result == "eq(agreement.product.id,order.product.id)"


def test_compare_null():
    query = RQLQuery(agreement__product__id=RQLProperty.null())

    result = str(query)

    assert result == "eq(agreement.product.id,null())"


def test_ne_quoted():
    query = RQLQuery("agreement.product.id")

    result = str(query.ne(RQLValue("order.product.id")))

    assert result == "ne(agreement.product.id,'order.product.id')"


def test_ne_property():
    query = RQLQuery("agreement.product.id")

    result = str(query.ne(RQLProperty("order.product.id")))

    assert result == "ne(agreement.product.id,order.product.id)"
