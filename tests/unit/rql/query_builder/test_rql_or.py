from decimal import Decimal

import pytest

from mpt_api_client.rql import RQLQuery


def test_or_empty():
    r1 = RQLQuery()
    r2 = RQLQuery()

    result = r1 | r2

    assert result == r1
    assert result == r2


def test_or_types():
    r1 = RQLQuery(id="ID")
    r2 = Decimal("32983.328238273")

    with pytest.raises(TypeError):
        r1 | r2


def test_or_equals():
    r1 = RQLQuery(id="ID")
    r2 = RQLQuery(id="ID")

    result = r1 | r2

    assert result == r1
    assert result == r2


def test_or_not_equals():
    r1 = RQLQuery(id="ID")
    r2 = RQLQuery(name="name")

    result = r1 | r2

    assert result != r1
    assert result != r2
    assert result.op == RQLQuery.OP_OR
    assert r1 in result.children
    assert r2 in result.children


def test_or_with_empty():
    result = RQLQuery(id="ID")

    assert result | RQLQuery() == result
    assert RQLQuery() | result == result


def test_or_merge():  # noqa: WPS210
    r1 = RQLQuery(id="ID")
    r2 = RQLQuery(name="name")
    r3 = RQLQuery(field="value")
    r4 = RQLQuery(field__in=("v1", "v2"))
    or1 = r1 | r2
    or2 = r3 | r4

    result = or1 | or2

    assert result.op == RQLQuery.OP_OR
    assert len(result.children) == 4
    assert [r1, r2, r3, r4] == result.children


def test_or_merge_duplicates():
    r1 = RQLQuery(id="ID")
    r2 = RQLQuery(field="value")

    result = r1 | r2 | r2

    assert len(result) == 2
    assert result.op == RQLQuery.OP_OR
    assert [r1, r2] == result.children
