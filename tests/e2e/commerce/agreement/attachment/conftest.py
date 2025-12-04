import pytest


@pytest.fixture
def invalid_agreement_attachment_id():
    return "ATT-0000-0000-0000-0000"


@pytest.fixture
def agreement_attachment_id(e2e_config):
    return e2e_config["commerce.agreement.attachment.id"]


@pytest.fixture
def agreement_attachment_factory():
    def factory(
        name: str = "E2E Created Agreement Attachment",
        attachment_type: str = "File",
        license_key: str = "",
    ):
        return {
            "name": name,
            "description": name,
            "type": attachment_type,
            "licenseKey": license_key,
        }

    return factory
