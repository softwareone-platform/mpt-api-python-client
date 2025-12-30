import pytest


@pytest.fixture
def invalid_ledger_attachment_id():
    return "LEA-0000-0000"


@pytest.fixture
def ledger_attachment_id(e2e_config):
    return e2e_config["billing.ledger.attachment.id"]


@pytest.fixture
def ledger_attachment_factory():
    def factory(
        name: str = "E2E Created Ledger Attachment",
    ):
        return {
            "name": name,
            "description": name,
        }

    return factory
