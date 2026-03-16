import httpx
import pytest
import respx

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.commerce.agreements import (
    Agreement,
    AgreementsService,
    AsyncAgreementsService,
)
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
                status_code=httpx.codes.OK,
                headers={"content-type": "text/markdown"},
                content=template_content,
            )
        )

        result = await async_agreements_service.template("AGR-123")

        assert result == template_content


def test_template(http_client):
    agreements_service = AgreementsService(http_client=http_client)
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/commerce/agreements/AGR-123/template"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "text/markdown"},
                content="# Order Template\n\nThis is a markdown template.",
            )
        )

        result = agreements_service.template("AGR-123")

        assert mock_route.called
        assert mock_route.call_count == 1
        assert result == "# Order Template\n\nThis is a markdown template."


def test_attachments_service(http_client):
    agreements_service = AgreementsService(http_client=http_client)

    result = agreements_service.attachments("AGR-123")

    assert isinstance(result, AgreementsAttachmentService)
    assert result.endpoint_params == {"agreement_id": "AGR-123"}


def test_async_attachments_service(http_client):
    agreements_service = AsyncAgreementsService(http_client=http_client)

    result = agreements_service.attachments("AGR-123")

    assert isinstance(result, AsyncAgreementsAttachmentService)
    assert result.endpoint_params == {"agreement_id": "AGR-123"}


@pytest.mark.parametrize("method", ["create", "update", "get", "render", "template"])
def test_mixins_present(http_client, method):
    service = AgreementsService(http_client=http_client)

    result = hasattr(service, method)

    assert result is True


@pytest.mark.parametrize("method", ["create", "update", "get", "render", "template"])
def test_async_mixins_present(async_http_client, method):
    service = AgreementsService(http_client=async_http_client)

    result = hasattr(service, method)

    assert result is True


@pytest.fixture
def agreement_data():
    return {
        "id": "AGR-001",
        "icon": "https://example.com/icon.png",
        "status": "Active",
        "name": "My Agreement",
        "startDate": "2024-01-01",
        "endDate": "2025-01-01",
        "listing": {"id": "LST-001"},
        "authorization": {"id": "AUT-001"},
        "vendor": {"id": "ACC-001"},
        "client": {"id": "ACC-002"},
        "price": {"total": 100},
        "template": {"id": "TPL-001"},
        "error": {"message": "some error"},
        "lines": [{"id": "LIN-001"}],
        "assets": [{"id": "ASS-001"}],
        "subscriptions": [{"id": "SUB-001"}],
        "parameters": {"fulfillment": []},
        "licensee": {"id": "ACC-003"},
        "buyer": {"id": "ACC-004"},
        "seller": {"id": "ACC-005"},
        "product": {"id": "PRD-001"},
        "externalIds": {"vendor": "ext-001"},
        "split": {"type": "none"},
        "termsAndConditions": [{"id": "TAC-001"}],
        "certificates": [{"id": "CRT-001"}],
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_agreement_primitive_fields(agreement_data):
    result = Agreement(agreement_data)

    assert result.to_dict() == agreement_data


def test_agreement_nested_party_fields(agreement_data):  # noqa: WPS218
    result = Agreement(agreement_data)

    assert isinstance(result.listing, BaseModel)
    assert isinstance(result.authorization, BaseModel)
    assert isinstance(result.vendor, BaseModel)
    assert isinstance(result.client, BaseModel)
    assert isinstance(result.price, BaseModel)


def test_agreement_nested_relation_fields(agreement_data):  # noqa: WPS218
    result = Agreement(agreement_data)

    assert isinstance(result.template, BaseModel)
    assert isinstance(result.error, BaseModel)
    assert isinstance(result.parameters, BaseModel)
    assert isinstance(result.licensee, BaseModel)
    assert isinstance(result.buyer, BaseModel)


def test_agreement_nested_identity_fields(agreement_data):  # noqa: WPS218
    result = Agreement(agreement_data)

    assert isinstance(result.seller, BaseModel)
    assert isinstance(result.product, BaseModel)
    assert isinstance(result.external_ids, BaseModel)
    assert isinstance(result.split, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_agreement_optional_fields_absent():
    result = Agreement({"id": "AGR-001"})

    assert result.id == "AGR-001"
    assert not hasattr(result, "name")
    assert not hasattr(result, "status")
    assert not hasattr(result, "audit")
