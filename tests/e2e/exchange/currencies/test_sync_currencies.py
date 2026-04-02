import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.models import FileModel
from tests.e2e.helper import assert_service_filter_with_iterate

pytestmark = [pytest.mark.flaky]


def test_create_currency(created_currency, currency_data):
    result = created_currency.code

    assert result == currency_data["code"]


def test_get_currency(currencies_service, currency_id):
    result = currencies_service.get(currency_id)

    assert result.id == currency_id


def test_get_currency_not_found(currencies_service):
    bogus_id = "CUR-0000-0000"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        currencies_service.get(bogus_id)


def test_update_currency(currencies_service, created_currency, logo_fd, short_uuid):
    update_data = {"name": f"e2e - please delete {short_uuid}"}

    result = currencies_service.update(created_currency.id, update_data, file=logo_fd)

    assert result.name == update_data["name"]


def test_delete_currency(currencies_service, created_currency):
    currencies_service.delete(created_currency.id)  # act


def test_filter_currencies(currencies_service, currency_id):
    assert_service_filter_with_iterate(currencies_service, currency_id, None)  # act


def test_download_icon(currencies_service, created_currency):
    result = currencies_service.download_icon(created_currency.id)

    assert isinstance(result, FileModel)
