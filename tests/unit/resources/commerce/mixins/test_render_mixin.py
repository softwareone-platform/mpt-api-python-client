import httpx
import respx

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.resources.commerce.mixins.render_mixin import AsyncRenderMixin, RenderMixin
from tests.unit.conftest import DummyModel


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


def test_render(http_client):
    service = DummyRenderService(http_client=http_client)
    rendered_content = "<h1>Dummy Rendered Content</h1>"
    with respx.mock:
        respx.get("https://api.example.com/public/v1/dummy/render/DUMMY-123/render").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "text/html"},
                content=rendered_content,
            )
        )

        result = service.render("DUMMY-123")

        assert result == rendered_content


async def test_async_render(async_http_client):
    service = AsyncDummyRenderService(http_client=async_http_client)
    rendered_content = "<h1>Dummy Rendered Content</h1>"
    with respx.mock:
        respx.get("https://api.example.com/public/v1/dummy/render/DUMMY-123/render").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "text/html"},
                content=rendered_content,
            )
        )

        result = await service.render("DUMMY-123")

        assert result == rendered_content
