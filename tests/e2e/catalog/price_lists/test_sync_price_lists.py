import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import (
    assert_service_filter_with_iterate,
    assert_update_resource,
)

pytestmark = [pytest.mark.flaky]


def test_create_price_list(created_price_list, product_id):
    result = created_price_list

    assert result.product.id == product_id


def test_get_price_list(price_lists_service, price_list_id):
    result = price_lists_service.get(price_list_id)

    assert result.id == price_list_id


def test_get_price_list_by_id(price_lists_service, price_list_id):
    result = price_lists_service.get(price_list_id)

    assert result.id == price_list_id


def test_iterate_price_lists(price_lists_service, price_list_id):
    price_lists = list(price_lists_service.iterate())

    result = any(price_list.id == price_list_id for price_list in price_lists)

    assert result is True


def test_filter_price_lists(price_lists_service, price_list_id):
    assert_service_filter_with_iterate(price_lists_service, price_list_id, ["-product"])  # act


def test_update_price_list(price_lists_service, price_list_id, short_uuid):
    assert_update_resource(
        price_lists_service, price_list_id, "notes", f"Updated notes {short_uuid}"
    )  # act


def test_delete_price_list(price_lists_service, created_price_list):
    price_lists_service.delete(created_price_list.id)  # act


def test_get_price_list_not_found(price_lists_service):
    bogus_id = "PRL-0000-NOTFOUND"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        price_lists_service.get(bogus_id)


def test_create_price_list_invalid_data(price_lists_service):
    invalid_data = {"name": "e2e - delete me"}

    with pytest.raises(MPTAPIError, match=r"400 One or more validation errors occurred"):
        price_lists_service.create(invalid_data)
