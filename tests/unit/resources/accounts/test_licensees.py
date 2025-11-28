import httpx
import pytest
import respx

from mpt_api_client.resources.accounts.licensees import AsyncLicenseesService, LicenseesService


@pytest.fixture
def licensees_service(http_client):
    return LicenseesService(http_client=http_client)


@pytest.fixture
def async_licensees_service(async_http_client):
    return AsyncLicenseesService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "delete", "update", "enable", "disable"],
)
def test_licensees_mixins_present(licensees_service, method):
    result = hasattr(licensees_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "delete", "update", "enable", "disable"],
)
def test_async_licensees_mixins_present(async_licensees_service, method):
    result = hasattr(async_licensees_service, method)

    assert result is True


def test_create_licensee(licensees_service, tmp_path):  # noqa: WPS210
    licensee_data = {
        "id": "LIC-0000-0001",
        "name": "Test E2E Licensee",
    }
    logo_path = tmp_path / "logo.png"
    logo_path.write_bytes(b"fake-logo-data")
    with logo_path.open("rb") as logo_file, respx.mock:
        mock_route = respx.post(licensees_service.path).mock(
            return_value=httpx.Response(httpx.codes.CREATED, json=licensee_data)
        )

        result = licensees_service.create(licensee_data, file=logo_file)

    request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert request.method == "POST"
    assert request.url.path == "/public/v1/accounts/licensees"
    assert result.to_dict() == licensee_data


def test_update_licensees(licensees_service, tmp_path):  # noqa: WPS210
    licensee_id = "BUY-0000-0001"
    licensee_data = {
        "name": "Updated Test licensee",
    }
    logo_path = tmp_path / "logo.png"
    logo_path.write_bytes(b"fake-logo-data")
    with logo_path.open("rb") as logo_file, respx.mock:
        mock_route = respx.put(f"{licensees_service.path}/{licensee_id}").mock(
            return_value=httpx.Response(httpx.codes.OK, json={"id": licensee_id, **licensee_data})
        )

        result = licensees_service.update(licensee_id, licensee_data, file=logo_file)

    request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert request.method == "PUT"
    assert request.url.path == f"/public/v1/accounts/licensees/{licensee_id}"
    assert result.to_dict() == {"id": licensee_id, **licensee_data}


async def test_async_create_licensees(async_licensees_service, tmp_path):  # noqa: WPS210
    licensee_data = {
        "id": "BUY-0000-0001",
        "name": "Test licensee",
    }
    logo_path = tmp_path / "logo.png"
    logo_path.write_bytes(b"fake-logo-data")
    with logo_path.open("rb") as logo_file, respx.mock:
        mock_route = respx.post(async_licensees_service.path).mock(
            return_value=httpx.Response(httpx.codes.CREATED, json=licensee_data)
        )

        licensee = await async_licensees_service.create(licensee_data, file=logo_file)

    request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert request.method == "POST"
    assert request.url.path == "/public/v1/accounts/licensees"
    assert licensee.to_dict() == licensee_data


async def test_async_update_licensees(async_licensees_service, tmp_path):  # noqa: WPS210
    licensee_id = "BUY-0000-0001"
    licensee_data = {
        "name": "Updated Test licensee",
    }
    logo_path = tmp_path / "logo.png"
    logo_path.write_bytes(b"fake-logo-data")
    with logo_path.open("rb") as logo_file, respx.mock:
        mock_route = respx.put(f"{async_licensees_service.path}/{licensee_id}").mock(
            return_value=httpx.Response(httpx.codes.OK, json={"id": licensee_id, **licensee_data})
        )

        licensee = await async_licensees_service.update(licensee_id, licensee_data, file=logo_file)

    request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert request.method == "PUT"
    assert request.url.path == f"/public/v1/accounts/licensees/{licensee_id}"
    assert licensee.to_dict() == {"id": licensee_id, **licensee_data}
