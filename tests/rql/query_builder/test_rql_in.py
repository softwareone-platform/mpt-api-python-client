from mpt_api_client.rql import RQLQuery


def test_in_and_namespaces():
    q1 = RQLQuery().n("agreement").n("product").n("id").in_(["PRD-1", "PRD-2"])  # noqa: WPS221
    q2 = RQLQuery().agreement.product.id.in_(["PRD-1", "PRD-2"])

    assert str(q1) == str(q2)


def test_in():
    products = ["PRD-1", "PRD-2"]
    product_ids = ",".join(products)
    query = RQLQuery(product__id__in=products)

    assert str(query) == f"in(product.id,({product_ids}))"
