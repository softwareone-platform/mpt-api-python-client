import pytest


@pytest.fixture
def attachment_id(e2e_config):
    return e2e_config["program.enrollment.attachment.id"]


@pytest.fixture
def invalid_attachment_id():
    return "ENA-0000-0000-0000-0000"


@pytest.fixture
def enrollment_attachment_factory():
    def factory(name: str = "E2E Created Program Enrollment Attachment"):
        return {
            "name": name,
            "description": name,
        }

    return factory
