from mpt_api_client.rql import RQLQuery


def test_and_or():  # noqa: WPS218 WPS473
    r1 = RQLQuery(id="ID")
    r2 = RQLQuery(field="value")

    r3 = RQLQuery(other="value2")
    r4 = RQLQuery(inop__in=("a", "b"))

    r5 = r1 & r2 & (r3 | r4)

    assert r5.op == RQLQuery.OP_AND
    assert str(r5) == "and(eq(id,ID),eq(field,value),or(eq(other,value2),in(inop,(a,b))))"  # noqa: WPS204

    r5 = r1 & r2 | r3

    assert str(r5) == "or(and(eq(id,ID),eq(field,value)),eq(other,value2))"

    r5 = r1 & (r2 | r3)

    assert str(r5) == "and(eq(id,ID),or(eq(field,value),eq(other,value2)))"

    r5 = (r1 & r2) | (r3 & r4)

    assert str(r5) == "or(and(eq(id,ID),eq(field,value)),and(eq(other,value2),in(inop,(a,b))))"

    r5 = (r1 & r2) | ~r3

    assert str(r5) == "or(and(eq(id,ID),eq(field,value)),not(eq(other,value2)))"


def test_and_merge():  # noqa: WPS210
    r1 = RQLQuery(id="ID")
    r2 = RQLQuery(name="name")

    r3 = RQLQuery(field="value")
    r4 = RQLQuery(field__in=("v1", "v2"))

    and1 = r1 & r2

    and2 = r3 & r4

    and3 = and1 & and2

    assert and3.op == RQLQuery.OP_AND
    assert len(and3.children) == 4
    assert [r1, r2, r3, r4] == and3.children
