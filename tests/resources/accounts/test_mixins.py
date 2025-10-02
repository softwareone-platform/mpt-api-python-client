import httpx
import pytest
import respx

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.resources.accounts.mixins import (
    ActivatableMixin,
    AsyncActivatableMixin,
    AsyncEnablableMixin,
    AsyncValidateMixin,
    EnablableMixin,
    ValidateMixin,
)
from tests.conftest import DummyModel


class DummyActivatableService(
    ActivatableMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/activatable/"
    _model_class = DummyModel
    _collection_key = "data"


class DummyAsyncActivatableService(
    AsyncActivatableMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/activatable/"
    _model_class = DummyModel
    _collection_key = "data"


class DummyEnablableService(
    EnablableMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/enablable/"
    _model_class = DummyModel
    _collection_key = "data"


class DummyAsyncEnablableService(
    AsyncEnablableMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/enablable/"
    _model_class = DummyModel
    _collection_key = "data"


class DummyValidateService(
    ValidateMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/validate/"
    _model_class = DummyModel
    _collection_key = "data"


class DummyAsyncValidateService(
    AsyncValidateMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/validate/"
    _model_class = DummyModel
    _collection_key = "data"


@pytest.fixture
def activatable_service(http_client):
    return DummyActivatableService(http_client=http_client)


@pytest.fixture
def async_activatable_service(async_http_client):
    return DummyAsyncActivatableService(http_client=async_http_client)


@pytest.fixture
def enablable_service(http_client):
    return DummyEnablableService(http_client=http_client)


@pytest.fixture
def async_enablable_service(async_http_client):
    return DummyAsyncEnablableService(http_client=async_http_client)


@pytest.fixture
def validate_service(http_client):
    return DummyValidateService(http_client=http_client)


@pytest.fixture
def async_validate_service(async_http_client):
    return DummyAsyncValidateService(http_client=async_http_client)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("activate", {"id": "OBJ-0000-0001", "status": "update"}),
        ("deactivate", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
def test_activatable_resource_actions(activatable_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/activatable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        activatable_obj = getattr(activatable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert activatable_obj.to_dict() == response_expected_data
        assert isinstance(activatable_obj, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("activate", None),
        ("deactivate", None),
    ],
)
def test_activatable_resource_actions_no_data(activatable_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/activatable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        activatable_obj = getattr(activatable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert activatable_obj.to_dict() == response_expected_data
        assert isinstance(activatable_obj, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("activate", {"id": "OBJ-0000-0001", "status": "update"}),
        ("deactivate", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
async def test_async_activatable_resource_actions(async_activatable_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/activatable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        activatable_obj = await getattr(async_activatable_service, action)(
            "OBJ-0000-0001", input_status
        )

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert activatable_obj.to_dict() == response_expected_data
        assert isinstance(activatable_obj, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("activate", None),
        ("deactivate", None),
    ],
)
async def test_async_activatable_resource_actions_no_data(
    async_activatable_service, action, input_status
):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/activatable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        activatable_obj = await getattr(async_activatable_service, action)(
            "OBJ-0000-0001", input_status
        )

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert activatable_obj.to_dict() == response_expected_data
        assert isinstance(activatable_obj, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("enable", {"id": "OBJ-0000-0001", "status": "update"}),
        ("disable", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
def test_enablable_resource_actions(enablable_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/enablable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        enablable_obj = getattr(enablable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert enablable_obj.to_dict() == response_expected_data
        assert isinstance(enablable_obj, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("enable", None),
        ("disable", None),
    ],
)
def test_enablable_resource_actions_no_data(enablable_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/enablable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        enablable_obj = getattr(enablable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert enablable_obj.to_dict() == response_expected_data
        assert isinstance(enablable_obj, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("enable", {"id": "OBJ-0000-0001", "status": "update"}),
        ("disable", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
async def test_async_enablable_resource_actions(async_enablable_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/enablable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        enablable_obj = await getattr(async_enablable_service, action)(
            "OBJ-0000-0001", input_status
        )

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert enablable_obj.to_dict() == response_expected_data
        assert isinstance(enablable_obj, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("enable", None),
        ("disable", None),
    ],
)
async def test_async_enablable_resource_actions_no_data(
    async_enablable_service, action, input_status
):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/enablable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        enablable_obj = await getattr(async_enablable_service, action)(
            "OBJ-0000-0001", input_status
        )

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert enablable_obj.to_dict() == response_expected_data
        assert isinstance(enablable_obj, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"), [("validate", {"id": "OBJ-0000-0001", "status": "update"})]
)
def test_validate_resource_actions(validate_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/validate/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        validate_obj = getattr(validate_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert validate_obj.to_dict() == response_expected_data
        assert isinstance(validate_obj, DummyModel)


@pytest.mark.parametrize(("action", "input_status"), [("validate", None)])
def test_validate_resource_actions_no_data(validate_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/validate/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        validate_obj = getattr(validate_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert validate_obj.to_dict() == response_expected_data
        assert isinstance(validate_obj, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"), [("validate", {"id": "OBJ-0000-0001", "status": "update"})]
)
async def test_async_validate_resource_actions(async_validate_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/validate/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        validate_obj = await getattr(async_validate_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert validate_obj.to_dict() == response_expected_data
        assert isinstance(validate_obj, DummyModel)


@pytest.mark.parametrize(("action", "input_status"), [("validate", None)])
async def test_async_validate_resource_actions_no_data(
    async_validate_service, action, input_status
):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/validate/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        validate_obj = await getattr(async_validate_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert validate_obj.to_dict() == response_expected_data
        assert isinstance(validate_obj, DummyModel)
