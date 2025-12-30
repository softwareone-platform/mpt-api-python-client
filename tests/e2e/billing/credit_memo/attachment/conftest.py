import pytest


@pytest.fixture
def invalid_credit_memo_attachment_id():
    return "CMA-0000-0000"


@pytest.fixture
def credit_memo_attachment_id(e2e_config):
    return e2e_config["billing.credit_memo.attachment.id"]


@pytest.fixture
def credit_memo_attachment_factory():
    def factory(
        name: str = "E2E Created Credit Memo Attachment",
    ):
        return {
            "name": name,
            "description": name,
        }

    return factory
