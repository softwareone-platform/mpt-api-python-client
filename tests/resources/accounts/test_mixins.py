import httpx
import pytest
import respx

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.resources.accounts.mixins import (
    ActivatableMixin,
    AsyncActivatableMixin,
    AsyncBlockableMixin,
    AsyncEnablableMixin,
    AsyncInvitableMixin,
    AsyncValidateMixin,
    BlockableMixin,
    EnablableMixin,
    InvitableMixin,
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


class DummyBlockableService(
    BlockableMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/blockable/"
    _model_class = DummyModel
    _collection_key = "data"


class DummyAsyncBlockableService(
    AsyncBlockableMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/blockable/"
    _model_class = DummyModel
    _collection_key = "data"


class DummyInvitableService(
    InvitableMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/invitable/"
    _model_class = DummyModel
    _collection_key = "data"


class DummyAsyncInvitableService(
    AsyncInvitableMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/invitable/"
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


@pytest.fixture
def blockable_service(http_client):
    return DummyBlockableService(http_client=http_client)


@pytest.fixture
def async_blockable_service(async_http_client):
    return DummyAsyncBlockableService(http_client=async_http_client)


@pytest.fixture
def invitable_service(http_client):
    return DummyInvitableService(http_client=http_client)


@pytest.fixture
def async_invitable_service(async_http_client):
    return DummyAsyncInvitableService(http_client=async_http_client)


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


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("block", {"id": "OBJ-0000-0001", "status": "update"}),
        ("unblock", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
def test_blockable_resource_actions(blockable_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/blockable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        blockable_obj = getattr(blockable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert blockable_obj.to_dict() == response_expected_data
        assert isinstance(blockable_obj, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("block", None),
        ("unblock", None),
    ],
)
def test_blockable_resource_actions_no_data(blockable_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/blockable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        blockable_obj = getattr(blockable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert blockable_obj.to_dict() == response_expected_data
        assert isinstance(blockable_obj, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("block", {"id": "OBJ-0000-0001", "status": "update"}),
        ("unblock", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
async def test_async_blockable_resource_actions(async_blockable_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/blockable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        blockable_obj = await getattr(async_blockable_service, action)(
            "OBJ-0000-0001", input_status
        )

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert blockable_obj.to_dict() == response_expected_data
        assert isinstance(blockable_obj, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("block", None),
        ("unblock", None),
    ],
)
async def test_async_blockable_resource_actions_no_data(
    async_blockable_service, action, input_status
):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/blockable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        blockable_obj = await getattr(async_blockable_service, action)(
            "OBJ-0000-0001", input_status
        )

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert blockable_obj.to_dict() == response_expected_data
        assert isinstance(blockable_obj, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("accept_invite", {"id": "OBJ-0000-0001", "status": "update"}),
        ("resend_invite", {"id": "OBJ-0000-0001", "status": "update"}),
        ("send_new_invite", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
def test_invitable_resource_actions(invitable_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/"
            f"dummy/invitable/OBJ-0000-0001/{action.replace('_', '-')}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        invitable_obj = getattr(invitable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert invitable_obj.to_dict() == response_expected_data
        assert isinstance(invitable_obj, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("accept_invite", None),
        ("resend_invite", None),
        ("send_new_invite", None),
    ],
)
def test_invitable_resource_actions_no_data(invitable_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/"
            f"dummy/invitable/OBJ-0000-0001/{action.replace('_', '-')}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        invitable_obj = getattr(invitable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert invitable_obj.to_dict() == response_expected_data
        assert isinstance(invitable_obj, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("accept_invite", {"id": "OBJ-0000-0001", "status": "update"}),
        ("resend_invite", {"id": "OBJ-0000-0001", "status": "update"}),
        ("send_new_invite", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
async def test_async_invitable_resource_actions(async_invitable_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/"
            f"dummy/invitable/OBJ-0000-0001/{action.replace('_', '-')}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        invitable_obj = await getattr(async_invitable_service, action)(
            "OBJ-0000-0001", input_status
        )

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert invitable_obj.to_dict() == response_expected_data
        assert isinstance(invitable_obj, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("accept_invite", None),
        ("resend_invite", None),
        ("send_new_invite", None),
    ],
)
async def test_async_invitable_resource_actions_no_data(
    async_invitable_service, action, input_status
):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/"
            f"dummy/invitable/OBJ-0000-0001/{action.replace('_', '-')}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        invitable_obj = await getattr(async_invitable_service, action)(
            "OBJ-0000-0001", input_status
        )

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert invitable_obj.to_dict() == response_expected_data
        assert isinstance(invitable_obj, DummyModel)
