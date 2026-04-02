import httpx
import pytest
import respx

from mpt_api_client.models import FileModel
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.exchange.currencies import (
    AsyncCurrenciesService,
    CurrenciesService,
    Currency,
)


@pytest.fixture
def currencies_service(http_client):
    return CurrenciesService(http_client=http_client)


@pytest.fixture
def async_currencies_service(async_http_client):
    return AsyncCurrenciesService(http_client=async_http_client)


@pytest.fixture
def currency_data():
    return {
        "id": "CUR-001",
        "name": "US Dollar",
        "code": "USD",
        "precision": 2,
        "statistics": {"sellerCount": 10, "pairCount": 5},
        "status": "Active",
        "icon": "https://example.com/icons/usd.png",
        "revision": 1,
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "iterate", "download_icon"],
)
def test_mixins_present(currencies_service, method):
    result = hasattr(currencies_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "iterate", "download_icon"],
)
def test_async_mixins_present(async_currencies_service, method):
    result = hasattr(async_currencies_service, method)

    assert result is True


def test_currency_primitive_fields(currency_data):
    result = Currency(currency_data)

    assert result.to_dict() == currency_data


@pytest.mark.parametrize("field", ["statistics", "audit"])
def test_currency_nested_model_fields(currency_data, field):
    result = Currency(currency_data)

    assert isinstance(getattr(result, field), BaseModel)


@pytest.mark.parametrize("field", ["name", "code", "audit"])
def test_currency_optional_fields_absent(field):
    result = Currency({"id": "CUR-001"})

    assert not hasattr(result, field)


def test_currency_id_present():
    result = Currency({"id": "CUR-001"})

    assert result.id == "CUR-001"


def test_get_currency(currencies_service):
    currency_id = "CUR-001"
    expected_response = {"id": currency_id, "name": "US Dollar", "code": "USD", "precision": 2}
    with respx.mock:
        respx.get(f"https://api.example.com/public/v1/exchange/currencies/{currency_id}").mock(
            return_value=httpx.Response(httpx.codes.OK, json=expected_response)
        )

        result = currencies_service.get(currency_id)

    assert result.to_dict() == expected_response


async def test_async_get_currency(async_currencies_service):
    currency_id = "CUR-001"
    expected_response = {"id": currency_id, "name": "US Dollar", "code": "USD", "precision": 2}
    with respx.mock:
        respx.get(f"https://api.example.com/public/v1/exchange/currencies/{currency_id}").mock(
            return_value=httpx.Response(httpx.codes.OK, json=expected_response)
        )

        result = await async_currencies_service.get(currency_id)

    assert result.to_dict() == expected_response


def test_create_currency(currencies_service, tmp_path):
    currency_data = {"name": "Euro", "code": "EUR", "precision": 2}
    expected_response = {"id": "CUR-002", "name": "Euro", "code": "EUR", "precision": 2}
    icon_path = tmp_path / "eur.png"
    icon_path.write_bytes(b"fake icon data")
    with icon_path.open("rb") as icon_file, respx.mock:
        respx.post("https://api.example.com/public/v1/exchange/currencies").mock(
            return_value=httpx.Response(httpx.codes.CREATED, json=expected_response)
        )

        result = currencies_service.create(currency_data, file=icon_file)

    assert result.to_dict() == expected_response


async def test_async_create_currency(async_currencies_service, tmp_path):
    currency_data = {"name": "British Pound", "code": "GBP", "precision": 2}
    expected_response = {"id": "CUR-003", "name": "British Pound", "code": "GBP", "precision": 2}
    icon_path = tmp_path / "gbp.png"
    icon_path.write_bytes(b"fake icon data")
    with icon_path.open("rb") as icon_file, respx.mock:
        respx.post("https://api.example.com/public/v1/exchange/currencies").mock(
            return_value=httpx.Response(httpx.codes.CREATED, json=expected_response)
        )

        result = await async_currencies_service.create(currency_data, file=icon_file)

    assert result.to_dict() == expected_response


def test_update_currency(currencies_service, tmp_path):
    currency_id = "CUR-001"
    update_data = {"name": "US Dollar Updated", "code": "USD", "precision": 2}
    expected_response = {
        "id": currency_id,
        "name": "US Dollar Updated",
        "code": "USD",
        "precision": 2,
    }
    icon_path = tmp_path / "usd.png"
    icon_path.write_bytes(b"updated icon data")
    with icon_path.open("rb") as icon_file, respx.mock:
        respx.put(f"https://api.example.com/public/v1/exchange/currencies/{currency_id}").mock(
            return_value=httpx.Response(httpx.codes.OK, json=expected_response)
        )

        result = currencies_service.update(currency_id, update_data, file=icon_file)

    assert result.to_dict() == expected_response


async def test_async_update_currency(async_currencies_service, tmp_path):
    currency_id = "CUR-001"
    update_data = {"name": "US Dollar Updated", "code": "USD", "precision": 2}
    expected_response = {
        "id": currency_id,
        "name": "US Dollar Updated",
        "code": "USD",
        "precision": 2,
    }
    icon_path = tmp_path / "usd.png"
    icon_path.write_bytes(b"updated icon data")
    with icon_path.open("rb") as icon_file, respx.mock:
        respx.put(f"https://api.example.com/public/v1/exchange/currencies/{currency_id}").mock(
            return_value=httpx.Response(httpx.codes.OK, json=expected_response)
        )

        result = await async_currencies_service.update(currency_id, update_data, file=icon_file)

    assert result.to_dict() == expected_response


def test_delete_currency(currencies_service):
    currency_id = "CUR-001"
    with respx.mock:
        mock_route = respx.delete(
            f"https://api.example.com/public/v1/exchange/currencies/{currency_id}"
        ).mock(return_value=httpx.Response(httpx.codes.NO_CONTENT))

        currencies_service.delete(currency_id)  # act

    assert mock_route.called is True


async def test_async_delete_currency(async_currencies_service):
    currency_id = "CUR-001"
    with respx.mock:
        mock_route = respx.delete(
            f"https://api.example.com/public/v1/exchange/currencies/{currency_id}"
        ).mock(return_value=httpx.Response(httpx.codes.NO_CONTENT))

        await async_currencies_service.delete(currency_id)  # act

    assert mock_route.called is True


def test_download_icon_returns_file_model(currencies_service):
    currency_id = "CUR-001"
    with respx.mock:
        respx.get(f"https://api.example.com/public/v1/exchange/currencies/{currency_id}/icon").mock(
            return_value=httpx.Response(
                httpx.codes.OK,
                content=b"PNG icon bytes",
                headers={"Content-Type": "image/png"},
            )
        )

        result = currencies_service.download_icon(currency_id)

    assert isinstance(result, FileModel)


def test_download_icon_returns_file_contents(currencies_service):
    currency_id = "CUR-001"
    icon_content = b"PNG icon bytes"
    with respx.mock:
        respx.get(f"https://api.example.com/public/v1/exchange/currencies/{currency_id}/icon").mock(
            return_value=httpx.Response(
                httpx.codes.OK,
                content=icon_content,
                headers={"Content-Type": "image/png"},
            )
        )

        result = currencies_service.download_icon(currency_id)

    assert result.file_contents == icon_content


async def test_async_download_icon_returns_file_model(async_currencies_service):
    currency_id = "CUR-001"
    with respx.mock:
        respx.get(f"https://api.example.com/public/v1/exchange/currencies/{currency_id}/icon").mock(
            return_value=httpx.Response(
                httpx.codes.OK,
                content=b"PNG icon bytes",
                headers={"Content-Type": "image/png"},
            )
        )

        result = await async_currencies_service.download_icon(currency_id)

    assert isinstance(result, FileModel)


async def test_async_download_icon_file_contents(async_currencies_service):
    currency_id = "CUR-001"
    icon_content = b"PNG icon bytes"
    with respx.mock:
        respx.get(f"https://api.example.com/public/v1/exchange/currencies/{currency_id}/icon").mock(
            return_value=httpx.Response(
                httpx.codes.OK,
                content=icon_content,
                headers={"Content-Type": "image/png"},
            )
        )

        result = await async_currencies_service.download_icon(currency_id)

    assert result.file_contents == icon_content
