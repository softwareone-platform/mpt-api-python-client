import httpx
import pytest
import respx

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.resources.commerce.mixins import (
    AsyncRenderMixin,
    AsyncTerminateMixin,
    RenderMixin,
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


class DummyRenderService(
    RenderMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "public/v1/dummy/render"
    _model_class = DummyModel


class AsyncDummyRenderService(
    AsyncRenderMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "public/v1/dummy/render"
    _model_class = DummyModel


@pytest.fixture
def dummy_terminate_service(http_client):
    return DummyTerminateService(http_client=http_client)


@pytest.fixture
def async_dummy_terminate_service(async_http_client):
    return AsyncDummyTerminateService(http_client=async_http_client)


@pytest.fixture
def dummy_render_service(http_client):
    return DummyRenderService(http_client=http_client)


@pytest.fixture
def async_dummy_render_service(async_http_client):
    return AsyncDummyRenderService(http_client=async_http_client)


def test_terminate_with_data(dummy_terminate_service):
    dummy_expected = {"id": "DUMMY-123", "status": "Terminated", "name": "Terminated DUMMY-123"}
    with respx.mock:
        respx.post("https://api.example.com/public/v1/dummy/terminate/DUMMY-123/terminate").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=dummy_expected,
            )
        )

        result = dummy_terminate_service.terminate("DUMMY-123", {"name": "Terminated DUMMY-123"})

        assert result.to_dict() == dummy_expected


def test_terminate(dummy_terminate_service):
    dummy_expected = {"id": "DUMMY-124", "status": "Terminated", "name": "Terminated DUMMY-124"}
    with respx.mock:
        respx.post("https://api.example.com/public/v1/dummy/terminate/DUMMY-124/terminate").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=dummy_expected,
            )
        )

        result = dummy_terminate_service.terminate("DUMMY-124")

        assert result.to_dict() == dummy_expected


async def test_async_terminate_with_data(async_dummy_terminate_service):
    dummy_expected = {"id": "DUMMY-123", "status": "Terminated", "name": "Terminated DUMMY-123"}
    with respx.mock:
        respx.post("https://api.example.com/public/v1/dummy/terminate/DUMMY-123/terminate").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=dummy_expected,
            )
        )

        result = await async_dummy_terminate_service.terminate(
            "DUMMY-123", {"name": "Terminated DUMMY-123"}
        )

        assert result.to_dict() == dummy_expected


async def test_async_terminate(async_dummy_terminate_service):
    dummy_expected = {"id": "DUMMY-124", "status": "Terminated", "name": "Terminated DUMMY-124"}
    with respx.mock:
        respx.post("https://api.example.com/public/v1/dummy/terminate/DUMMY-124/terminate").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=dummy_expected,
            )
        )

        result = await async_dummy_terminate_service.terminate("DUMMY-124")

        assert result.to_dict() == dummy_expected


def test_render(dummy_render_service):
    rendered_content = "<h1>Dummy Rendered Content</h1>"
    with respx.mock:
        respx.get("https://api.example.com/public/v1/dummy/render/DUMMY-123/render").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "text/html"},
                content=rendered_content,
            )
        )

        result = dummy_render_service.render("DUMMY-123")

        assert result == rendered_content


async def test_async_render(async_dummy_render_service):
    rendered_content = "<h1>Dummy Rendered Content</h1>"
    with respx.mock:
        respx.get("https://api.example.com/public/v1/dummy/render/DUMMY-123/render").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "text/html"},
                content=rendered_content,
            )
        )

        result = await async_dummy_render_service.render("DUMMY-123")

        assert result == rendered_content
