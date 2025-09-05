import httpx
import pytest
import respx

from mpt_api_client.resources.commerce.agreements import AgreementsService, AsyncAgreementsService
from mpt_api_client.resources.commerce.agreements_attachments import (
    AgreementsAttachmentService,
    AsyncAgreementsAttachmentService,
)


async def test_async_template(async_http_client):
    async_agreements_service = AsyncAgreementsService(http_client=async_http_client)
    template_content = "# Order Template\n\nThis is a markdown template."
    with respx.mock:
        respx.get("https://api.example.com/public/v1/commerce/agreements/AGR-123/template").mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "text/markdown"},
                content=template_content,
            )
        )

        template = await async_agreements_service.template("AGR-123")

        assert template == template_content


def test_template(http_client):
    agreements_service = AgreementsService(http_client=http_client)
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/commerce/agreements/AGR-123/template"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "text/markdown"},
                content="# Order Template\n\nThis is a markdown template.",
            )
        )

        markdown_template = agreements_service.template("AGR-123")

        assert mock_route.called
        assert mock_route.call_count == 1
        assert markdown_template == "# Order Template\n\nThis is a markdown template."


def test_attachments_service(http_client):
    agreements_service = AgreementsService(http_client=http_client)

    attachments = agreements_service.attachments("AGR-123")

    assert isinstance(attachments, AgreementsAttachmentService)
    assert attachments.endpoint_params == {"agreement_id": "AGR-123"}


def test_async_attachments_service(http_client):
    agreements_service = AsyncAgreementsService(http_client=http_client)

    attachments = agreements_service.attachments("AGR-123")

    assert isinstance(attachments, AsyncAgreementsAttachmentService)
    assert attachments.endpoint_params == {"agreement_id": "AGR-123"}


@pytest.mark.parametrize("method", ["create", "update", "get"])
def test_mixins_present(http_client, method):
    service = AgreementsService(http_client=http_client)
    assert hasattr(service, method)


@pytest.mark.parametrize("method", ["create", "update", "get"])
def test_async_mixins_present(async_http_client, method):
    service = AgreementsService(http_client=async_http_client)
    assert hasattr(service, method)
