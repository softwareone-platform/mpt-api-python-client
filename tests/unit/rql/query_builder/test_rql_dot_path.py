import datetime as dt
from decimal import Decimal

import pytest

from mpt_api_client.rql import RQLQuery


@pytest.mark.parametrize("op", ["eq", "ne", "gt", "ge", "le", "lt"])
def test_dotted_path_comp(op):
    class Test:  # noqa: WPS431
        pass  # noqa: WPS604 WPS420

    # BL
    test = Test()
    today = dt.datetime.now(dt.UTC).date()
    now = dt.datetime.now(dt.UTC)
    today_expected_result = f"{op}(asset.id,'{today.isoformat()}')"
    now_expected_result = f"{op}(asset.id,'{now.isoformat()}')"

    with pytest.raises(TypeError):
        getattr(RQLQuery().asset.id, op)(test)

    assert str(getattr(RQLQuery().asset.id, op)(today)) == today_expected_result
    assert str(getattr(RQLQuery().asset.id, op)(now)) == now_expected_result


@pytest.mark.parametrize("op", ["eq", "ne", "gt", "ge", "le", "lt"])
def test_dotted_path_comp_bool_and_str(op):
    result = getattr(RQLQuery().asset.id, op)

    assert str(result("value")) == f"{op}(asset.id,'value')"
    assert str(result(True)) == f"{op}(asset.id,'true')"  # noqa: FBT003
    assert str(result(False)) == f"{op}(asset.id,'false')"  # noqa: FBT003


@pytest.mark.parametrize("op", ["eq", "ne", "gt", "ge", "le", "lt"])  # noqa: AAA01
def test_dotted_path_comp_numerics(op):
    decimal_object = Decimal("32983.328238273")
    attribute_op_match = getattr(RQLQuery().asset.id, op)

    integer_result = str(attribute_op_match(10))
    result_float = str(attribute_op_match(10.678937))
    decimal_result = str(attribute_op_match(Decimal("32983.328238273")))

    assert integer_result == f"{op}(asset.id,'10')"
    assert result_float == f"{op}(asset.id,'10.678937')"
    assert decimal_result == f"{op}(asset.id,'{decimal_object!s}')"


@pytest.mark.parametrize("op", ["like", "ilike"])
def test_dotted_path_search(op):
    result = getattr(RQLQuery().asset.id, op)

    assert str(result("value")) == f"{op}(asset.id,value)"
    assert str(result("*value")) == f"{op}(asset.id,*value)"
    assert str(result("value*")) == f"{op}(asset.id,value*)"
    assert str(result("*value*")) == f"{op}(asset.id,*value*)"


@pytest.mark.parametrize(
    ("method", "op"),
    [
        ("in_", "in"),
        ("oneof", "in"),
        ("out", "out"),
    ],
)
def test_dotted_path_list(method, op):  # noqa: AAA01
    rexpr_set = getattr(RQLQuery().asset.id, method)(("first", "second"))
    rexpr_list = getattr(RQLQuery().asset.id, method)(["first", "second"])

    with pytest.raises(TypeError):
        getattr(RQLQuery().asset.id, method)("Test")

    assert str(rexpr_set) == f"{op}(asset.id,(first,second))"
    assert str(rexpr_list) == f"{op}(asset.id,(first,second))"


@pytest.mark.parametrize(
    ("expr", "expression_param", "expected_op"),
    [
        ("null", True, "eq"),
        ("null", False, "ne"),
        ("empty", True, "eq"),
        ("empty", False, "ne"),
    ],
)
def test_dotted_path_bool(expr, expression_param, expected_op):
    expected_result = f"{expected_op}(asset.id,{expr}())"
    attribute = getattr(RQLQuery().asset.id, expr)

    result = str(attribute(expression_param))

    assert result == expected_result


def test_dotted_path_already_evaluated():
    query = RQLQuery().first.second.eq("value")

    with pytest.raises(AttributeError):
        query.third  # noqa: B018
