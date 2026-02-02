import httpx
import respx

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.resources.commerce.mixins.terminate_mixin import (
    AsyncTerminateMixin,
    TerminateMixin,
)
from tests.unit.conftest import DummyModel


class DummyTerminateService(
    TerminateMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "public/v1/dummy/terminate"
    _model_class = DummyModel


class AsyncDummyTerminateService(
    AsyncTerminateMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "public/v1/dummy/terminate"
    _model_class = DummyModel


def test_terminate_with_data(http_client):
    service = DummyTerminateService(http_client=http_client)
    dummy_expected = {"id": "DUMMY-123", "status": "Terminated", "name": "Terminated DUMMY-123"}
    with respx.mock:
        respx.post("https://api.example.com/public/v1/dummy/terminate/DUMMY-123/terminate").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=dummy_expected,
            )
        )

        result = service.terminate("DUMMY-123", {"name": "Terminated DUMMY-123"})

        assert result.to_dict() == dummy_expected


def test_terminate(http_client):
    service = DummyTerminateService(http_client=http_client)
    dummy_expected = {"id": "DUMMY-124", "status": "Terminated", "name": "Terminated DUMMY-124"}
    with respx.mock:
        respx.post("https://api.example.com/public/v1/dummy/terminate/DUMMY-124/terminate").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=dummy_expected,
            )
        )

        result = service.terminate("DUMMY-124")

        assert result.to_dict() == dummy_expected


async def test_async_terminate_with_data(async_http_client):
    service = AsyncDummyTerminateService(http_client=async_http_client)
    dummy_expected = {"id": "DUMMY-123", "status": "Terminated", "name": "Terminated DUMMY-123"}
    with respx.mock:
        respx.post("https://api.example.com/public/v1/dummy/terminate/DUMMY-123/terminate").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=dummy_expected,
            )
        )

        result = await service.terminate("DUMMY-123", {"name": "Terminated DUMMY-123"})

        assert result.to_dict() == dummy_expected


async def test_async_terminate(async_http_client):
    service = AsyncDummyTerminateService(http_client=async_http_client)
    dummy_expected = {"id": "DUMMY-124", "status": "Terminated", "name": "Terminated DUMMY-124"}
    with respx.mock:
        respx.post("https://api.example.com/public/v1/dummy/terminate/DUMMY-124/terminate").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=dummy_expected,
            )
        )

        result = await service.terminate("DUMMY-124")

        assert result.to_dict() == dummy_expected
