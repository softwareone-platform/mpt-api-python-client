from mpt_api_client.rql import RQLProperty, RQLQuery, RQLValue


def test_repr():  # noqa: AAA01
    products = ["PRD-1", RQLValue("PRD-2"), RQLProperty("agreement.product.id")]
    expression_query = RQLQuery(product__id__in=products)
    or_expression = RQLQuery(name="Albert") | RQLQuery(surname="Einstein")

    assert (
        repr(expression_query)
        == "<RQLQuery(expr) in(product.id,('PRD-1','PRD-2',agreement.product.id))>"
    )
    assert repr(or_expression) == "<RQLQuery(or)>"


def test_len():  # noqa: AAA01
    empty_query = RQLQuery()
    simple_query = RQLQuery(id="ID")
    complex_query = RQLQuery(id="ID", status__in=("a", "b"))

    assert len(empty_query) == 0
    assert len(simple_query) == 1
    assert len(complex_query) == 2


def test_bool():  # noqa: AAA01
    assert bool(RQLQuery()) is False
    assert bool(RQLQuery(id="ID")) is True
    assert bool(RQLQuery(id="ID", status__in=("a", "b"))) is True


def test_str():  # noqa: AAA01
    assert str(RQLQuery(id="ID")) == "eq(id,'ID')"
    assert str(~RQLQuery(id="ID")) == "not(eq(id,'ID'))"
    assert str(~RQLQuery(id="ID", field="value")) == "not(and(eq(id,'ID'),eq(field,'value')))"
    assert not str(RQLQuery())


def test_hash():
    query_set = set()

    result = RQLQuery(id="ID", field="value")

    query_set.add(result)
    query_set.add(result)
    assert len(query_set) == 1


def test_empty():  # noqa: AAA01
    assert RQLQuery("value").empty() == RQLQuery("value").empty()
    assert str(RQLQuery("value1").empty()) == "eq(value1,empty())"
    assert str(RQLQuery("value2").not_empty()) == "ne(value2,empty())"
    assert RQLQuery("value3").empty(value=False) == RQLQuery("value3").not_empty()
