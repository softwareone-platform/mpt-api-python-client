from decimal import Decimal

import pytest

from mpt_api_client.rql import RQLQuery


def test_and_types():
    r1 = RQLQuery(id="ID")
    r2 = Decimal("32983.328238273")

    with pytest.raises(TypeError):
        r1 & r2


def test_and_both_empty():
    r1 = RQLQuery()
    r2 = RQLQuery()

    r3 = r1 & r2

    assert r3 == r1
    assert r3 == r2


def test_and_duplicates():
    r1 = RQLQuery(id="ID")
    r2 = RQLQuery(id="ID")

    r3 = r1 & r2

    assert r3 == r1
    assert r3 == r2


def test_and_different():
    r1 = RQLQuery(id="ID")
    r2 = RQLQuery(name="name")

    r3 = r1 & r2

    assert r3 != r1
    assert r3 != r2
    assert r3.op == RQLQuery.OP_AND
    assert r1 in r3.children
    assert r2 in r3.children


def test_and_with_empty():
    rql = RQLQuery(id="ID")

    assert rql & RQLQuery() == rql
    assert RQLQuery() & rql == rql


def test_and_triple():
    r1 = RQLQuery(id="ID")
    r2 = RQLQuery(field="value")

    r3 = r1 & r2 & r2

    assert len(r3) == 2
    assert r3.op == RQLQuery.OP_AND
    assert [r1, r2] == r3.children
