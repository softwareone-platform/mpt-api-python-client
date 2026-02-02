import pytest

from mpt_api_client import RQLQuery
from tests.unit.http.conftest import DummyService


def test_queryable_mixin_order_by(dummy_service: DummyService) -> None:
    result = dummy_service.order_by("created", "-name")

    assert result != dummy_service
    assert dummy_service.query_state.order_by is None
    assert result.query_state.order_by == ["created", "-name"]
    assert result.http_client is dummy_service.http_client
    assert result.endpoint_params == dummy_service.endpoint_params


def test_queryable_mixin_order_by_exception(dummy_service: DummyService) -> None:
    """Test that setting order_by multiple times raises an exception."""
    ordered_service = dummy_service.order_by("created")

    with pytest.raises(
        ValueError, match=r"Ordering is already set. Cannot set ordering multiple times."
    ):
        ordered_service.order_by("name")


def test_queryable_mixin_filter(
    dummy_service: DummyService, filter_status_active: RQLQuery
) -> None:
    result = dummy_service.filter(filter_status_active)

    assert result != dummy_service
    assert dummy_service.query_state.filter is None
    assert result.query_state.filter == filter_status_active
    assert result.http_client is dummy_service.http_client
    assert result.endpoint_params == dummy_service.endpoint_params


def test_queryable_mixin_filters(dummy_service: DummyService) -> None:
    """Test applying multiple filters to a queryable service."""
    filter1 = RQLQuery(status="active")
    filter2 = RQLQuery(name="test")

    result = dummy_service.filter(filter1).filter(filter2)

    assert dummy_service.query_state.filter is None
    assert result.query_state.filter == filter1 & filter2


def test_queryable_mixin_select(dummy_service: DummyService) -> None:
    result = dummy_service.select("id", "name", "-audit")

    assert result != dummy_service
    assert dummy_service.query_state.select is None
    assert result.query_state.select == ["id", "name", "-audit"]
    assert result.http_client is dummy_service.http_client
    assert result.endpoint_params == dummy_service.endpoint_params


def test_queryable_mixin_select_exception(dummy_service: DummyService) -> None:
    """Test that setting select fields multiple times raises an exception."""
    selected_service = dummy_service.select("id", "name")

    with pytest.raises(
        ValueError, match=r"Select fields are already set. Cannot set select fields multiple times."
    ):
        selected_service.select("other_field")


def test_queryable_mixin_method_chaining(
    dummy_service: DummyService, filter_status_active: RQLQuery
) -> None:
    result = (
        dummy_service.filter(filter_status_active).order_by("created", "-name").select("id", "name")
    )

    assert result != dummy_service
    assert result.query_state.filter == filter_status_active
    assert result.query_state.order_by == ["created", "-name"]
    assert result.query_state.select == ["id", "name"]
