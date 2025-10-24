from decimal import Decimal

import pytest

from mpt_api_client.rql import RQLQuery


def test_or_empty():
    r1 = RQLQuery()
    r2 = RQLQuery()

    r3 = r1 | r2

    assert r3 == r1
    assert r3 == r2


def test_or_types():
    r1 = RQLQuery(id="ID")
    r2 = Decimal("32983.328238273")

    with pytest.raises(TypeError):
        r1 | r2


def test_or_equals():
    r1 = RQLQuery(id="ID")
    r2 = RQLQuery(id="ID")

    r3 = r1 | r2

    assert r3 == r1
    assert r3 == r2


def test_or_not_equals():
    r1 = RQLQuery(id="ID")
    r2 = RQLQuery(name="name")

    r3 = r1 | r2

    assert r3 != r1
    assert r3 != r2

    assert r3.op == RQLQuery.OP_OR
    assert r1 in r3.children
    assert r2 in r3.children


def test_or_with_empty():
    rql = RQLQuery(id="ID")

    assert rql | RQLQuery() == rql
    assert RQLQuery() | rql == rql


def test_or_merge():  # noqa: WPS210
    r1 = RQLQuery(id="ID")
    r2 = RQLQuery(name="name")

    r3 = RQLQuery(field="value")
    r4 = RQLQuery(field__in=("v1", "v2"))

    or1 = r1 | r2
    or2 = r3 | r4
    or3 = or1 | or2

    assert or3.op == RQLQuery.OP_OR
    assert len(or3.children) == 4
    assert [r1, r2, r3, r4] == or3.children


def test_or_merge_duplicates():
    r1 = RQLQuery(id="ID")
    r2 = RQLQuery(field="value")

    r3 = r1 | r2 | r2

    assert len(r3) == 2
    assert r3.op == RQLQuery.OP_OR
    assert [r1, r2] == r3.children
