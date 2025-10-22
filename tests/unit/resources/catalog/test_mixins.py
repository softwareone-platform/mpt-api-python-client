import httpx
import pytest
import respx

from mpt_api_client.http.async_service import AsyncService
from mpt_api_client.http.service import Service
from mpt_api_client.resources.catalog.mixins import (
    ActivatableMixin,
    AsyncActivatableMixin,
    AsyncPublishableMixin,
    PublishableMixin,
)
from tests.unit.conftest import DummyModel


class DummyPublishableService(  # noqa: WPS215
    PublishableMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/publishable/"
    _model_class = DummyModel
    _collection_key = "data"


class DummyAsyncPublishableService(  # noqa: WPS215
    AsyncPublishableMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/publishable/"
    _model_class = DummyModel
    _collection_key = "data"


class DummyActivatableService(  # noqa: WPS215
    ActivatableMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/activatable/"
    _model_class = DummyModel
    _collection_key = "data"


class DummyAsyncActivatableService(  # noqa: WPS215
    AsyncActivatableMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/activatable/"
    _model_class = DummyModel
    _collection_key = "data"


@pytest.fixture
def publishable_service(http_client):
    return DummyPublishableService(http_client=http_client)


@pytest.fixture
def async_publishable_service(async_http_client):
    return DummyAsyncPublishableService(http_client=async_http_client)


@pytest.fixture
def activatable_service(http_client):
    return DummyActivatableService(http_client=http_client)


@pytest.fixture
def async_activatable_service(async_http_client):
    return DummyAsyncActivatableService(http_client=async_http_client)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("review", {"id": "PRD-123", "status": "update"}),
        ("publish", {"id": "PRD-123", "status": "update"}),
        ("unpublish", {"id": "PRD-123", "status": "update"}),
    ],
)
def test_custom_resource_actions(publishable_service, action, input_status):
    request_expected_content = b'{"id":"PRD-123","status":"update"}'
    response_expected_data = {"id": "PRD-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/publishable/PRD-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        order = getattr(publishable_service, action)("PRD-123", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert order.to_dict() == response_expected_data
        assert isinstance(order, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("review", None),
        ("publish", None),
        ("unpublish", None),
    ],
)
def test_custom_resource_actions_no_data(publishable_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "PRD-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/publishable/PRD-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        order = getattr(publishable_service, action)("PRD-123")

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert order.to_dict() == response_expected_data
        assert isinstance(order, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("review", {"id": "PRD-123", "status": "update"}),
        ("publish", {"id": "PRD-123", "status": "update"}),
        ("unpublish", {"id": "PRD-123", "status": "update"}),
    ],
)
async def test_async_custom_resource_actions(async_publishable_service, action, input_status):
    request_expected_content = b'{"id":"PRD-123","status":"update"}'
    response_expected_data = {"id": "PRD-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/publishable/PRD-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        order = await getattr(async_publishable_service, action)("PRD-123", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert order.to_dict() == response_expected_data
        assert isinstance(order, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("review", None),
        ("publish", None),
        ("unpublish", None),
    ],
)
async def test_async_custom_resource_actions_no_data(
    async_publishable_service, action, input_status
):
    request_expected_content = b""
    response_expected_data = {"id": "PRD-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/publishable/PRD-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        order = await getattr(async_publishable_service, action)("PRD-123")

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert order.to_dict() == response_expected_data
        assert isinstance(order, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("activate", {"id": "OBJ-0000-0001", "status": "update"}),
        ("deactivate", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
def test_custom_resource_activatable_actions(activatable_service, action, input_status):
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
        attachment = getattr(activatable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert attachment.to_dict() == response_expected_data
        assert isinstance(attachment, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("activate", None),
        ("deactivate", None),
    ],
)
def test_custom_resource_activatable_actions_no_data(activatable_service, action, input_status):
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
        attachment = getattr(activatable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert attachment.to_dict() == response_expected_data
        assert isinstance(attachment, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("activate", {"id": "OBJ-0000-0001", "status": "update"}),
        ("deactivate", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
async def test_async_custom_resource_activatable_actions(
    async_activatable_service, action, input_status
):
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
        attachment = await getattr(async_activatable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert attachment.to_dict() == response_expected_data
        assert isinstance(attachment, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("activate", None),
        ("deactivate", None),
    ],
)
async def test_async_custom_resource_activatable_actions_no_data(
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
        attachment = await getattr(async_activatable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert attachment.to_dict() == response_expected_data
        assert isinstance(attachment, DummyModel)
