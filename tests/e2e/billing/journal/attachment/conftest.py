import pytest


@pytest.fixture
def invalid_journal_attachment_id():
    return "JOA-0000-0000"


@pytest.fixture
def journal_attachment_id(e2e_config):
    return e2e_config["billing.journal.attachment.id"]


@pytest.fixture
def journal_attachment_factory():
    def factory(
        name: str = "E2E Created Journal Attachment",
    ):
        return {
            "name": name,
            "description": name,
        }

    return factory
