import httpx
import pytest
import respx

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCreateFileMixin,
    AsyncUpdateFileMixin,
    CreateFileMixin,
    UpdateFileMixin,
)
from mpt_api_client.resources.accounts.mixins import (
    ActivatableMixin,
    AsyncActivatableMixin,
    AsyncBlockableMixin,
    AsyncInvitableMixin,
    AsyncValidateMixin,
    BlockableMixin,
    InvitableMixin,
    ValidateMixin,
)
from tests.unit.conftest import DummyModel


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


class DummyCreateFileService(
    CreateFileMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/create-file/"
    _model_class = DummyModel
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "resource"


class AsyncDummyCreateFileService(
    AsyncCreateFileMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/create-file/"
    _model_class = DummyModel
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "resource"


class DummyUpdateFileService(
    UpdateFileMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/update-file/"
    _model_class = DummyModel
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "resource"


class DummyAsyncUpdateFileService(
    AsyncUpdateFileMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/update-file/"
    _model_class = DummyModel
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "resource"


@pytest.fixture
def activatable_service(http_client):
    return DummyActivatableService(http_client=http_client)


@pytest.fixture
def async_activatable_service(async_http_client):
    return DummyAsyncActivatableService(http_client=async_http_client)


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


@pytest.fixture
def create_file_service(http_client):
    return DummyCreateFileService(http_client=http_client)


@pytest.fixture
def async_create_file_service(async_http_client):
    return AsyncDummyCreateFileService(http_client=async_http_client)


@pytest.fixture
def update_file_service(http_client):
    return DummyUpdateFileService(http_client=http_client)


@pytest.fixture
def async_update_file_service(async_http_client):
    return DummyAsyncUpdateFileService(http_client=async_http_client)


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

        result = getattr(activatable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


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

        result = getattr(activatable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


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

        result = await getattr(async_activatable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


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

        result = await getattr(async_activatable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


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

        result = getattr(validate_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


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

        result = getattr(validate_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


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

        result = await getattr(async_validate_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


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

        result = await getattr(async_validate_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


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

        result = getattr(blockable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


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

        result = getattr(blockable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


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

        result = await getattr(async_blockable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


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

        result = await getattr(async_blockable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


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

        result = getattr(invitable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


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

        result = getattr(invitable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


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

        result = await getattr(async_invitable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


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

        result = await getattr(async_invitable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


def test_create_file_service(create_file_service, tmp_path):  # noqa: WPS210
    resource_data = {"name": "Test File"}
    response_expected_data = {"id": "OBJ-0000-0001", **resource_data}
    with respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/dummy/create-file/").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        file_path = tmp_path / "file.png"
        file_path.write_bytes(b"fake-file-data")

        with file_path.open("rb") as file_file:
            result = create_file_service.create(resource_data, file_file)

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


def test_create_file_service_no_file(create_file_service):
    resource_data = {"name": "Test File"}
    response_expected_data = {"id": "OBJ-0000-0001", **resource_data}
    with respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/dummy/create-file/").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = create_file_service.create(resource_data, None)

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


async def test_async_create_file_service(async_create_file_service, tmp_path):  # noqa: WPS210
    resource_data = {"name": "Test File"}
    response_expected_data = {"id": "OBJ-0000-0001", **resource_data}
    with respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/dummy/create-file/").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        file_path = tmp_path / "file.png"
        file_path.write_bytes(b"fake-file-data")

        with file_path.open("rb") as file_file:
            result = await async_create_file_service.create(resource_data, file_file)

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


async def test_async_create_file_service_no_file(async_create_file_service):
    resource_data = {"name": "Test File"}
    response_expected_data = {"id": "OBJ-0000-0001", **resource_data}
    with respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/dummy/create-file/").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        result = await async_create_file_service.create(resource_data, None)

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


def test_update_file_service(update_file_service, tmp_path):  # noqa: WPS210
    resource_data = {"name": "Test File"}
    response_expected_data = {"id": "OBJ-0000-0001", **resource_data}
    with respx.mock:
        mock_route = respx.put(
            "https://api.example.com/public/v1/dummy/update-file/OBJ-0000-0001"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        update_file_path = tmp_path / "file.png"
        update_file_path.write_bytes(b"updated file content")

        with update_file_path.open("rb") as update_file:
            result = update_file_service.update("OBJ-0000-0001", resource_data, update_file)

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


def test_update_file_service_no_file(update_file_service):
    resource_data = {"name": "Test File"}
    response_expected_data = {"id": "OBJ-0000-0001", **resource_data}
    with respx.mock:
        mock_route = respx.put(
            "https://api.example.com/public/v1/dummy/update-file/OBJ-0000-0001"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = update_file_service.update("OBJ-0000-0001", resource_data, None)

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


async def test_async_update_file_service(async_update_file_service, tmp_path):  # noqa: WPS210
    resource_data = {"name": "Test File"}
    response_expected_data = {"id": "OBJ-0000-0001", **resource_data}
    with respx.mock:
        mock_route = respx.put(
            "https://api.example.com/public/v1/dummy/update-file/OBJ-0000-0001"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        update_file_path = tmp_path / "file.png"
        update_file_path.write_bytes(b"updated file content")

        with update_file_path.open("rb") as update_file:
            result = await async_update_file_service.update(
                "OBJ-0000-0001", resource_data, update_file
            )

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


async def test_async_update_file_service_no_file(async_update_file_service):
    resource_data = {"name": "Test File"}
    response_expected_data = {"id": "OBJ-0000-0001", **resource_data}
    with respx.mock:
        mock_route = respx.put(
            "https://api.example.com/public/v1/dummy/update-file/OBJ-0000-0001"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        result = await async_update_file_service.update("OBJ-0000-0001", resource_data, None)

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)
