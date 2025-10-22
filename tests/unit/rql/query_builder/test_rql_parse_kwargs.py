import pytest

from mpt_api_client.rql.query_builder import parse_kwargs


@pytest.fixture
def mock_product_ids_for_expression():
    return ["PRD-1", "PRD-2"]


@pytest.fixture
def mock_product_id_for_expression():
    return "PRD-1"


def test_improper_op(mock_product_id_for_expression):
    products_expr = {"product__id__inn": mock_product_id_for_expression}
    query = parse_kwargs(products_expr)

    assert str(query) == f"['eq(product.id.inn,{mock_product_id_for_expression})']"


def test_parse_eq(mock_product_id_for_expression):
    products_expr = {"product__id__eq": mock_product_id_for_expression}
    query = parse_kwargs(products_expr)

    assert str(query) == f"['eq(product.id,{mock_product_id_for_expression})']"


def test_parse_like(mock_product_id_for_expression):
    products_expr = {"product__id__like": mock_product_id_for_expression}
    query = parse_kwargs(products_expr)

    assert str(query) == f"['like(product.id,{mock_product_id_for_expression})']"


def test_parse_null_op(mock_product_id_for_expression):
    products_expr = {"product__id__null": mock_product_id_for_expression}
    query = parse_kwargs(products_expr)

    assert str(query) == "['ne(product.id,null())']"
