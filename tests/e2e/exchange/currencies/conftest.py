import logging
import secrets
import string

import pytest
from iso4217 import Currency

from mpt_api_client.exceptions import MPTAPIError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CURRENCY_CODE_LENGTH = 3
CURRENCY_CODE_ALPHABET = string.ascii_uppercase
ISO_CURRENCY_CODES = frozenset(currency.code for currency in Currency)


def _random_currency_code():
    while True:
        letters = (secrets.choice(CURRENCY_CODE_ALPHABET) for _ in range(CURRENCY_CODE_LENGTH))
        code = "".join(letters)
        if code not in ISO_CURRENCY_CODES:
            return code


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
    code = _random_currency_code()
    logger.info("e2e generated currency code: %s", code)
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
        logger.warning("TEARDOWN - Unable to delete currency %s: %s", currency.id, error.title)


@pytest.fixture
async def async_created_currency(async_currencies_service, currency_data, logo_fd):
    currency = await async_currencies_service.create(currency_data, file=logo_fd)

    yield currency

    try:
        await async_currencies_service.delete(currency.id)
    except MPTAPIError as error:
        logger.warning("TEARDOWN - Unable to delete currency %s: %s", currency.id, error.title)
