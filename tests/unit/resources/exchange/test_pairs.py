import httpx
import pytest
import respx

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.exchange.pairs import AsyncPairsService, Pair, PairsService


@pytest.fixture
def pairs_service(http_client):
    return PairsService(http_client=http_client)


@pytest.fixture
def async_pairs_service(async_http_client):
    return AsyncPairsService(http_client=async_http_client)


@pytest.fixture
def pair_data():
    return {
        "id": "PAI-001",
        "name": "USD/EUR",
        "externalId": "EXT-001",
        "notes": "Primary conversion pair",
        "primary": True,
        "reverse": {"id": "PAI-002", "name": "EUR/USD"},
        "sourceCurrency": {"id": "CUR-001", "code": "USD"},
        "destinationCurrency": {"id": "CUR-002", "code": "EUR"},
        "latestRate": {"id": "RAT-001", "value": 0.92},
        "agreements": 3,
        "rates": 12,
        "status": "Active",
        "revision": 1,
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


@pytest.mark.parametrize("method", ["get", "fetch_page", "fetch_one", "iterate"])
def test_mixins_present(pairs_service, method):
    result = hasattr(pairs_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "fetch_page", "fetch_one", "iterate"])
def test_async_mixins_present(async_pairs_service, method):
    result = hasattr(async_pairs_service, method)

    assert result is True


def test_pairs_service_endpoint(pairs_service):
    result = pairs_service.build_path()

    assert result == "/public/v1/exchange/pairs"


def test_async_pairs_service_endpoint(async_pairs_service):
    result = async_pairs_service.build_path()

    assert result == "/public/v1/exchange/pairs"


def test_pair_primitive_fields(pair_data):
    result = Pair(pair_data)

    assert result.to_dict() == pair_data


@pytest.mark.parametrize("field", ["name", "external_id", "notes", "status"])
def test_pair_string_fields(pair_data, field):
    result = Pair(pair_data)

    assert isinstance(getattr(result, field), str)


@pytest.mark.parametrize("field", ["agreements", "rates", "revision"])
def test_pair_integer_fields(pair_data, field):
    result = Pair(pair_data)

    assert isinstance(getattr(result, field), int)


def test_pair_primary_field(pair_data):
    result = Pair(pair_data)

    assert result.primary is True


@pytest.mark.parametrize(
    "field",
    ["reverse", "source_currency", "destination_currency", "latest_rate", "audit"],
)
def test_pair_nested_model_fields(pair_data, field):
    result = Pair(pair_data)

    assert isinstance(getattr(result, field), BaseModel)


@pytest.mark.parametrize("field", ["name", "external_id", "status", "audit"])
def test_pair_optional_fields_absent(field):
    result = Pair({"id": "PAI-001"})

    assert not hasattr(result, field)


def test_pair_id_present():
    result = Pair({"id": "PAI-001"})

    assert result.id == "PAI-001"


def test_get_pair(pairs_service):
    pair_id = "PAI-001"
    expected_response = {"id": pair_id, "name": "USD/EUR", "primary": True}
    with respx.mock:
        respx.get(f"https://api.example.com/public/v1/exchange/pairs/{pair_id}").mock(
            return_value=httpx.Response(httpx.codes.OK, json=expected_response)
        )

        result = pairs_service.get(pair_id)

    assert result.to_dict() == expected_response


async def test_async_get_pair(async_pairs_service):
    pair_id = "PAI-001"
    expected_response = {"id": pair_id, "name": "USD/EUR", "primary": True}
    with respx.mock:
        respx.get(f"https://api.example.com/public/v1/exchange/pairs/{pair_id}").mock(
            return_value=httpx.Response(httpx.codes.OK, json=expected_response)
        )

        result = await async_pairs_service.get(pair_id)

    assert result.to_dict() == expected_response


def test_fetch_page_pairs(pairs_service):
    expected_pairs = [{"id": "PAI-001", "name": "USD/EUR"}, {"id": "PAI-002", "name": "EUR/USD"}]
    with respx.mock:
        respx.get("https://api.example.com/public/v1/exchange/pairs").mock(
            return_value=httpx.Response(
                httpx.codes.OK,
                json={"data": expected_pairs, "$meta": {"pagination": {"total": 2}}},
            )
        )

        result = pairs_service.fetch_page()

    assert [pair.to_dict() for pair in result] == expected_pairs


async def test_async_fetch_page_pairs(async_pairs_service):
    expected_pairs = [{"id": "PAI-001", "name": "USD/EUR"}, {"id": "PAI-002", "name": "EUR/USD"}]
    with respx.mock:
        respx.get("https://api.example.com/public/v1/exchange/pairs").mock(
            return_value=httpx.Response(
                httpx.codes.OK,
                json={"data": expected_pairs, "$meta": {"pagination": {"total": 2}}},
            )
        )

        result = await async_pairs_service.fetch_page()

    assert [pair.to_dict() for pair in result] == expected_pairs
