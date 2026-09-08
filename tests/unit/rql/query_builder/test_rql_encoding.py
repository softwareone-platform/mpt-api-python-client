import datetime as dt
from decimal import Decimal

import pytest

from mpt_api_client.rql import RQLProperty, RQLQuery

# Every character that is a delimiter in a URI query component or in an RQL expression,
# paired with the encoding that has to reach the wire so it travels as data instead.
SPECIAL_VALUES = (
    pytest.param("A&B", "A%26B", id="ampersand splits the query"),
    pytest.param("a#b", "a%23b", id="hash truncates the query"),
    pytest.param("a+b", "a%2Bb", id="plus decodes to a space"),
    pytest.param("50%", "50%25", id="trailing percent"),
    pytest.param("%d1", "%25d1", id="percent escape lookalike"),
    pytest.param("a,b", "a%2Cb", id="comma separates list items"),
    pytest.param("a(b)", "a%28b%29", id="parentheses group an expression"),
    pytest.param("a=b", "a%3Db", id="equals"),
    pytest.param("a;b", "a%3Bb", id="semicolon"),
    pytest.param("a?b", "a%3Fb", id="question mark"),
    pytest.param("a b", "a%20b", id="space"),
    pytest.param("Grün", "Gr%C3%BCn", id="non-ascii"),
)


@pytest.mark.parametrize(("raw", "encoded"), SPECIAL_VALUES)
def test_eq_encodes_value(raw, encoded):
    result = str(RQLQuery(name=raw))

    assert result == f"eq(name,'{encoded}')"


@pytest.mark.parametrize(("raw", "encoded"), SPECIAL_VALUES)
def test_in_encodes_every_list_value(raw, encoded):
    result = str(RQLQuery().name.in_([raw, raw]))

    assert result == f"in(name,('{encoded}','{encoded}'))"


@pytest.mark.parametrize(("raw", "encoded"), SPECIAL_VALUES)
def test_like_encodes_value_around_wildcard(raw, encoded):
    result = str(RQLQuery().name.like(f"*{raw}*"))

    assert result == f"like(name,'*{encoded}*')"


# A value carrying a quote cannot rely on percent-encoding: the server decodes the query
# parameter before parsing the RQL expression, so %27 reaches the parser as a quote. The
# literal switches delimiter instead, and a value carrying both quotes is inexpressible.
QUOTED_VALUES = (
    pytest.param("O'Brien", '"O%27Brien"', id="single quote -> double-quoted literal"),
    pytest.param('say "hi"', "'say%20%22hi%22'", id="double quote -> single-quoted literal"),
    pytest.param("Maria's Super Store", '"Maria%27s%20Super%20Store"', id="real buyer name"),
)


@pytest.mark.parametrize(("raw", "literal"), QUOTED_VALUES)
def test_quote_selects_the_delimiter(raw, literal):
    result = str(RQLQuery(name=raw))

    assert result == f"eq(name,{literal})"


@pytest.mark.parametrize(("raw", "literal"), QUOTED_VALUES)
def test_quote_selects_the_delimiter_in_list(raw, literal):
    result = str(RQLQuery().name.in_([raw]))

    assert result == f"in(name,({literal}))"


@pytest.mark.parametrize(("raw", "literal"), QUOTED_VALUES)
def test_quote_selects_the_delimiter_in_search(raw, literal):
    result = str(RQLQuery().name.like(raw))

    assert result == f"like(name,{literal})"


def test_both_quotes_rejected():
    with pytest.raises(ValueError, match="cannot contain both a single and a double quote"):
        RQLQuery(name='Standard & Poor\'s "AAA" rating')


def test_both_quotes_rejected_in_list():
    with pytest.raises(ValueError, match="cannot contain both a single and a double quote"):
        RQLQuery().name.in_(["fine", 'O\'Brien said "hi"'])


@pytest.mark.parametrize("op", ["like", "ilike"])
def test_search_keeps_the_wildcard_literal(op):
    result = str(getattr(RQLQuery().name, op)("*value*"))

    assert result == f"{op}(name,'*value*')"


def test_datetime_offset_sign_encoded():
    moment = dt.datetime(2026, 9, 8, 10, 30, 15, tzinfo=dt.UTC)

    result = str(RQLQuery(created=moment))

    assert result == "eq(created,'2026-09-08T10%3A30%3A15%2B00%3A00')"


def test_date_needs_no_encoding():
    result = str(RQLQuery(created=dt.date(2026, 9, 8)))

    assert result == "eq(created,'2026-09-08')"


def test_decimal_exponent_sign_encoded():
    result = str(RQLQuery(price=Decimal("1E+3")))

    assert result == "eq(price,1E%2B3)"


def test_kwargs_field_name_encoded():
    query_dict = {"na&me": "reference"}

    result = str(RQLQuery(**query_dict))

    assert result == "eq(na%26me,'reference')"


def test_kwargs_operator_field_name_encoded():
    query_dict = {"na&me__like": "reference"}

    result = str(RQLQuery(**query_dict))

    assert result == "like(na%26me,'reference')"


def test_dotted_field_name_encoded_per_segment():
    result = str(RQLQuery().n("agreement.pro&duct.id").eq("value"))

    assert result == "eq(agreement.pro%26duct.id,'value')"


def test_list_field_name_encoded():
    result = str(RQLQuery().n("pro&duct").in_(["a", "b"]))

    assert result == "in(pro%26duct,('a','b'))"


def test_empty_field_name_encoded():
    result = str(RQLQuery().n("pro&duct").empty())

    assert result == "eq(pro%26duct,empty())"


def test_nested_collection_name_encoded():
    result = str(RQLQuery(orderQty__gt=1).any("sale&Details"))

    assert result == "any(sale%26Details,gt(orderQty,1))"


def test_property_field_path_encoded():
    result = str(RQLQuery(name=RQLProperty("order.pro&duct.id")))

    assert result == "eq(name,order.pro%26duct.id)"


@pytest.mark.parametrize("operator", ["null()", "empty()"])
def test_operator_property_not_encoded(operator):
    result = str(RQLQuery(name=RQLProperty(operator)))

    assert result == f"eq(name,{operator})"


def test_null_property_stays_an_operator():
    result = str(RQLQuery(name=RQLProperty.null()))

    assert result == "eq(name,null())"
