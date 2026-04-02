import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.models import FileModel
from tests.e2e.helper import assert_async_service_filter_with_iterate

pytestmark = [pytest.mark.flaky]


def test_create_currency(async_created_currency, currency_data):
    result = async_created_currency.code

    assert result == currency_data["code"]


async def test_get_currency(async_currencies_service, currency_id):
    result = await async_currencies_service.get(currency_id)

    assert result.id == currency_id


async def test_get_currency_not_found(async_currencies_service):
    bogus_id = "CUR-0000-0000"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_currencies_service.get(bogus_id)


async def test_update_currency(
    async_currencies_service, async_created_currency, logo_fd, short_uuid
):
    update_data = {"name": f"e2e - please delete {short_uuid}"}

    result = await async_currencies_service.update(
        async_created_currency.id, update_data, file=logo_fd
    )

    assert result.name == update_data["name"]


async def test_delete_currency(async_currencies_service, async_created_currency):
    await async_currencies_service.delete(async_created_currency.id)  # act


async def test_filter_currencies(async_currencies_service, currency_id):
    await assert_async_service_filter_with_iterate(
        async_currencies_service, currency_id, None
    )  # act


async def test_download_icon(async_currencies_service, async_created_currency):
    result = await async_currencies_service.download_icon(async_created_currency.id)

    assert isinstance(result, FileModel)
