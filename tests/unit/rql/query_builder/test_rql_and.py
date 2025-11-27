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

    result = r1 & r2

    assert result == r1
    assert result == r2


def test_and_duplicates():
    r1 = RQLQuery(id="ID")
    r2 = RQLQuery(id="ID")

    result = r1 & r2

    assert result == r1
    assert result == r2


def test_and_different():
    r1 = RQLQuery(id="ID")
    r2 = RQLQuery(name="name")

    result = r1 & r2

    assert result != r1
    assert result != r2
    assert result.op == RQLQuery.OP_AND
    assert r1 in result.children
    assert r2 in result.children


def test_and_with_empty():
    result = RQLQuery(id="ID")

    assert result & RQLQuery() == result
    assert RQLQuery() & result == result


def test_and_triple():
    r1 = RQLQuery(id="ID")
    r2 = RQLQuery(field="value")

    result = r1 & r2 & r2

    assert len(result) == 2
    assert result.op == RQLQuery.OP_AND
    assert [r1, r2] == result.children
