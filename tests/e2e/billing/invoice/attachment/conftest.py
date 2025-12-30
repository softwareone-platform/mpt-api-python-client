import pytest


@pytest.fixture
def invalid_invoice_attachment_id():
    return "IVA-0000-0000"


@pytest.fixture
def invoice_attachment_id(e2e_config):
    return e2e_config["billing.invoice.attachment.id"]


@pytest.fixture
def invoice_attachment_factory():
    def factory(
        name: str = "E2E Created Invoice Attachment",
    ):
        return {
            "name": name,
            "description": name,
        }

    return factory
