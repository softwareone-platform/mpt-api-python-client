import string

import pytest

from mpt_api_client.exceptions import MPTAPIError


@pytest.fixture
def currencies_service(mpt_ops):
    return mpt_ops.exchange.currencies


@pytest.fixture
def async_currencies_service(async_mpt_ops):
    return async_mpt_ops.exchange.currencies


@pytest.fixture(scope="session")
def currency_id(e2e_config):
    return e2e_config["exchange.currency.id"]


@pytest.fixture
def currency_data(short_uuid):
    digit_to_alpha = str.maketrans(string.digits, "GHIJKLMNOP")
    code = short_uuid[:3].translate(digit_to_alpha).upper()
    return {
        "name": f"e2e - please delete {short_uuid}",
        "code": code,
        "precision": 2,
    }


@pytest.fixture
def created_currency(currencies_service, currency_data, logo_fd):
    currency = currencies_service.create(currency_data, file=logo_fd)

    yield currency

    try:
        currencies_service.delete(currency.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete currency {currency.id}: {error.title}")  # noqa: WPS421


@pytest.fixture
async def async_created_currency(async_currencies_service, currency_data, logo_fd):
    currency = await async_currencies_service.create(currency_data, file=logo_fd)

    yield currency

    try:
        await async_currencies_service.delete(currency.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete currency {currency.id}: {error.title}")  # noqa: WPS421
