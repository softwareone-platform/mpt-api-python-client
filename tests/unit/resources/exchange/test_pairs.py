import json

import httpx
import pytest
import respx

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.exchange.pairs import AsyncPairsService, Pair, PairsService
from mpt_api_client.resources.exchange.rates import AsyncRatesService, RatesService
from mpt_api_client.rql import RQLQuery

# The VND:USD pair exactly as the platform returns it, kept as JSON text so the rate values
# stay the wire representation rather than becoming float literals in the test source.
PAIR_JSON = """
{
  "id": "FXP-0001-0231",
  "name": "VND:USD",
  "revision": 490,
  "primary": false,
  "reverse": {
    "id": "FXP-0000-0231",
    "name": "USD:VND",
    "revision": 490,
    "primary": true,
    "sourceCurrency": {
      "id": "CUR-0048", "name": "United States dollar",
      "revision": 8, "code": "USD", "precision": 2
    },
    "destinationCurrency": {
      "id": "CUR-0050", "name": "Vietnamese dong",
      "revision": 1, "code": "VND", "precision": 0
    },
    "latestRate": {"id": "FXR-9287-0354-2104", "revision": 2, "value": 25903.03970661}
  },
  "sourceCurrency": {
    "id": "CUR-0050", "name": "Vietnamese dong",
    "revision": 1, "code": "VND", "precision": 0
  },
  "destinationCurrency": {
    "id": "CUR-0048", "name": "United States dollar",
    "revision": 8, "code": "USD", "precision": 2
  },
  "latestRate": {"id": "FXR-6327-9235-1166", "revision": 2, "value": 3.861e-05},
  "agreements": 0,
  "rates": 216,
  "status": "Active"
}
"""


@pytest.fixture
def pairs_service(http_client):
    return PairsService(http_client=http_client)


@pytest.fixture
def async_pairs_service(async_http_client):
    return AsyncPairsService(http_client=async_http_client)


@pytest.fixture
def pair_data():
    return json.loads(PAIR_JSON)


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate", "rates"])
def test_mixins_present(pairs_service, method):
    result = hasattr(pairs_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate", "rates"])
def test_async_mixins_present(async_pairs_service, method):
    result = hasattr(async_pairs_service, method)

    assert result is True


def test_pair_primitive_fields(pair_data):
    result = Pair(pair_data)

    assert result.to_dict() == pair_data


@pytest.mark.parametrize(
    "field",
    ["source_currency", "destination_currency", "latest_rate", "reverse"],
)
def test_pair_nested_model_fields(pair_data, field):
    result = Pair(pair_data)

    assert isinstance(getattr(result, field), BaseModel)


def test_pair_latest_rate_is_reachable(pair_data):
    result = Pair(pair_data)

    assert str(result.latest_rate.value) == "3.861e-05"


def test_pair_reverse_latest_rate_is_reachable(pair_data):
    result = Pair(pair_data)

    assert str(result.reverse.latest_rate.value) == "25903.03970661"


def test_pair_currency_codes_are_reachable(pair_data):
    result = Pair(pair_data)

    assert (result.source_currency.code, result.destination_currency.code) == ("VND", "USD")


def test_pair_currency_refs_are_snake_cased(pair_data):
    result = Pair(pair_data)

    assert result.to_dict()["sourceCurrency"]["code"] == "VND"


@pytest.mark.parametrize("field", ["name", "source_currency", "latest_rate"])
def test_pair_optional_fields_absent(field):
    result = Pair({"id": "FXP-0000-0001"})

    assert not hasattr(result, field)


def test_get_pair(pairs_service, pair_data):
    with respx.mock:
        respx.get("https://api.example.com/public/v1/exchange/pairs/FXP-0001-0231").mock(
            return_value=httpx.Response(httpx.codes.OK, json=pair_data)
        )

        result = pairs_service.get("FXP-0001-0231")

    assert result.to_dict() == pair_data


async def test_async_get_pair(async_pairs_service, pair_data):
    with respx.mock:
        respx.get("https://api.example.com/public/v1/exchange/pairs/FXP-0001-0231").mock(
            return_value=httpx.Response(httpx.codes.OK, json=pair_data)
        )

        result = await async_pairs_service.get("FXP-0001-0231")

    assert result.to_dict() == pair_data


def test_list_pairs_filtered_by_currency_codes(pairs_service, pair_data):
    """The API accepts only ``sourceCurrency.code``/``destinationCurrency.code``.

    Any other spelling, ``source.code`` included, is rejected with a 400 Invalid property path.
    """
    query = RQLQuery(sourceCurrency__code="VND", destinationCurrency__code="USD")
    with respx.mock:
        route = respx.get(url__startswith="https://api.example.com/public/v1/exchange/pairs").mock(
            return_value=httpx.Response(httpx.codes.OK, json={"data": [pair_data]})
        )

        result = pairs_service.filter(query).fetch_page()

    assert [pair.to_dict() for pair in result] == [pair_data]
    assert "eq(sourceCurrency.code,'VND')" in str(route.calls[0].request.url)
    assert "eq(destinationCurrency.code,'USD')" in str(route.calls[0].request.url)


def test_rates_returns_scoped_service(pairs_service):
    result = pairs_service.rates("FXP-0000-0001")

    assert isinstance(result, RatesService)
    assert result.path == "/public/v1/exchange/pairs/FXP-0000-0001/rates"


def test_async_rates_returns_scoped_service(async_pairs_service):
    result = async_pairs_service.rates("FXP-0000-0001")

    assert isinstance(result, AsyncRatesService)
    assert result.path == "/public/v1/exchange/pairs/FXP-0000-0001/rates"


def test_rates_shares_the_http_client(pairs_service):
    result = pairs_service.rates("FXP-0000-0001")

    assert result.http_client is pairs_service.http_client
