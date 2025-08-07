from decimal import Decimal

from mpt_api_client.rql import RQLQuery


def test_eq_object():
    r1 = RQLQuery(id="ID")
    r2 = Decimal("32983.328238273")

    assert r1 != r2


def test_eq_empty():
    r1 = RQLQuery()
    r2 = RQLQuery()

    assert r1 == r2


def test_eq_id():
    r1 = RQLQuery(id="ID")
    r2 = RQLQuery(id="ID")

    assert r1 == r2


def test_eq_id_negated():
    r1 = ~RQLQuery(id="ID")
    r2 = ~RQLQuery(id="ID")

    assert r1 == r2


def test_eq_status_in():
    r1 = RQLQuery(id="ID", status__in=("a", "b"))
    r2 = RQLQuery(id="ID", status__in=("a", "b"))

    assert r1 == r2


def test_not_eq_status_in():
    r1 = RQLQuery()
    r2 = RQLQuery(id="ID", status__in=("a", "b"))

    assert r1 != r2
