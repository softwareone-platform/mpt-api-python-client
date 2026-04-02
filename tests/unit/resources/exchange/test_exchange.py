import pytest

from mpt_api_client.resources.exchange.currencies import (
    AsyncCurrenciesService,
    CurrenciesService,
)
from mpt_api_client.resources.exchange.exchange import AsyncExchange, Exchange


@pytest.fixture
def exchange(http_client):
    return Exchange(http_client=http_client)


@pytest.fixture
def async_exchange(async_http_client):
    return AsyncExchange(http_client=async_http_client)


def test_exchange_initialization(http_client):
    result = Exchange(http_client=http_client)

    assert result.http_client is http_client


def test_async_exchange_initialization(async_http_client):
    result = AsyncExchange(http_client=async_http_client)

    assert result.http_client is async_http_client


def test_exchange_currencies_property(exchange):
    result = exchange.currencies

    assert isinstance(result, CurrenciesService)
    assert result.http_client is exchange.http_client


def test_async_exchange_currencies_property(async_exchange):
    result = async_exchange.currencies

    assert isinstance(result, AsyncCurrenciesService)
    assert result.http_client is async_exchange.http_client
