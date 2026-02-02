import httpx
import respx

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.resources.commerce.mixins.template_mixin import (
    AsyncTemplateMixin,
    TemplateMixin,
)
from tests.unit.conftest import DummyModel


class DummyTemplateService(
    TemplateMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "public/v1/dummy/template"
    _model_class = DummyModel


class AsyncDummyTemplateService(
    AsyncTemplateMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "public/v1/dummy/template"
    _model_class = DummyModel


def test_template(http_client):
    service = DummyTemplateService(http_client=http_client)
    template_content = "<h1>Dummy Template Content</h1>"
    with respx.mock:
        respx.get("https://api.example.com/public/v1/dummy/template/DUMMY-123/template").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                content=template_content,
            )
        )

        result = service.template("DUMMY-123")

        assert result == template_content


async def test_async_template(async_http_client):
    service = AsyncDummyTemplateService(http_client=async_http_client)
    template_content = "<h1>Dummy Template Content</h1>"
    with respx.mock:
        respx.get("https://api.example.com/public/v1/dummy/template/DUMMY-123/template").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                content=template_content,
            )
        )

        result = await service.template("DUMMY-123")

        assert result == template_content
