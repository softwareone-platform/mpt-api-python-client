import pytest


@pytest.fixture
def custom_ledger_attachment_id(e2e_config):
    return e2e_config["billing.custom_ledger.attachment.id"]


@pytest.fixture
def invalid_custom_ledger_attachment_id():
    return "CLA-0000-0000"


@pytest.fixture
def custom_ledger_attachment_factory():
    def factory(
        name: str = "E2E Created Custom Ledger Attachment",
    ):
        return {
            "name": name,
            "description": name,
        }

    return factory
