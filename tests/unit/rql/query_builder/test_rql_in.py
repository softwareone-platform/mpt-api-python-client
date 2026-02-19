from mpt_api_client.rql import Property, RQLQuery


def test_in_and_namespaces():
    q1 = RQLQuery().n("agreement").n("product").n("id").in_(["PRD-1", "PRD-2"])  # noqa: WPS221
    q2 = RQLQuery().agreement.product.id.in_(["PRD-1", "PRD-2"])

    result = str(q1) == str(q2)

    assert result is True


def test_in():
    products = ["PRD-1", "PRD-2", Property("product.id")]

    result = RQLQuery(product__id__in=products)

    assert str(result) == "in(product.id,('PRD-1','PRD-2',product.id))"
