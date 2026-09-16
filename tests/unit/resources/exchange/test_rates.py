import json

import httpx
import pytest
import respx

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.exchange.rates import AsyncRatesService, Rate, RatesService
from mpt_api_client.rql import RQLQuery

PAIR_ID = "FXP-1671-0642"
RATES_URL = f"https://api.example.com/public/v1/exchange/pairs/{PAIR_ID}/rates"

# A rate exactly as the platform returns it: the amount lives under `value`, as a JSON number.
# Kept as JSON text so the rate stays the wire representation rather than a float literal.
RATE_JSON = """
{
  "id": "FXR-0010-7429-8190",
  "revision": 2,
  "recordDate": "2026-02-20T00:00:00.000Z",
  "value": 0.23130512,
  "status": "Active",
  "reverseRate": {"id": "FXR-6961-1679-3921", "revision": 2, "value": 4.32329379}
}
"""


@pytest.fixture
def rates_service(http_client):
    return RatesService(http_client=http_client, endpoint_params={"pair_id": PAIR_ID})


@pytest.fixture
def async_rates_service(async_http_client):
    return AsyncRatesService(http_client=async_http_client, endpoint_params={"pair_id": PAIR_ID})


@pytest.fixture
def rate_data():
    return json.loads(RATE_JSON)


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate"])
def test_mixins_present(rates_service, method):
    result = hasattr(rates_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate"])
def test_async_mixins_present(async_rates_service, method):
    result = hasattr(async_rates_service, method)

    assert result is True


def test_rate_primitive_fields(rate_data):
    result = Rate(rate_data)

    assert result.to_dict() == rate_data


def test_rate_reverse_rate_is_nested_model(rate_data):
    result = Rate(rate_data)

    assert isinstance(result.reverse_rate, BaseModel)


def test_rate_reverse_value_is_reachable(rate_data):
    result = Rate(rate_data)

    assert str(result.reverse_rate.value) == "4.32329379"


def test_rate_record_date_is_snake_cased(rate_data):
    result = Rate(rate_data)

    assert result.record_date == "2026-02-20T00:00:00.000Z"


def test_rate_value_is_kept_uncoerced(rate_data):
    result = Rate(rate_data)

    assert isinstance(result.value, float)


def test_rate_value_survives_exponent_form():
    result = Rate(json.loads('{"id": "FXR-0001", "value": 3.861e-05}'))

    assert str(result.value) == "3.861e-05"


def test_endpoint_is_scoped_to_the_pair(rates_service):
    result = rates_service.path

    assert result == f"/public/v1/exchange/pairs/{PAIR_ID}/rates"


def test_get_rate(rates_service, rate_data):
    with respx.mock:
        respx.get(f"{RATES_URL}/FXR-1671-0642-0000").mock(
            return_value=httpx.Response(httpx.codes.OK, json=rate_data)
        )

        result = rates_service.get("FXR-1671-0642-0000")

    assert result.to_dict() == rate_data


async def test_async_get_rate(async_rates_service, rate_data):
    with respx.mock:
        respx.get(f"{RATES_URL}/FXR-1671-0642-0000").mock(
            return_value=httpx.Response(httpx.codes.OK, json=rate_data)
        )

        result = await async_rates_service.get("FXR-1671-0642-0000")

    assert result.to_dict() == rate_data


def test_list_rates(rates_service, rate_data):
    with respx.mock:
        respx.get(url__startswith=RATES_URL).mock(
            return_value=httpx.Response(httpx.codes.OK, json={"data": [rate_data]})
        )

        result = rates_service.fetch_page()

    assert [rate.to_dict() for rate in result] == [rate_data]


def test_list_rates_filtered_by_record_date(rates_service, rate_data):
    """Filters carry the API's own field spelling, as everywhere else in the client.

    ``Rate.record_date`` is the deserialized attribute name; RQL field names are never
    case-converted, so a caller filters on ``recordDate``.
    """
    query = RQLQuery(recordDate__gt="2024-05-09")
    with respx.mock:
        route = respx.get(url__startswith=RATES_URL).mock(
            return_value=httpx.Response(httpx.codes.OK, json={"data": [rate_data]})
        )

        result = rates_service.filter(query).fetch_page()

    assert [rate.to_dict() for rate in result] == [rate_data]
    assert "gt(recordDate,'2024-05-09')" in str(route.calls[0].request.url)
