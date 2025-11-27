import pytest

from mpt_api_client.exceptions import MPTAPIError


@pytest.fixture
def attachment_id(created_attachment):
    return created_attachment.id


@pytest.fixture
def attachment_data():
    return {
        "name": "e2e test attachment - please delete",
        "description": "E2E test attachment for automated testing",
    }


@pytest.fixture
def attachment_service(mpt_ops, pricing_policy_id):
    return mpt_ops.catalog.pricing_policies.attachments(pricing_policy_id)


@pytest.fixture
def created_attachment(attachment_service, attachment_data, pdf_fd):
    attachment = attachment_service.create(attachment_data, file=pdf_fd)
    yield attachment
    try:
        attachment_service.delete(attachment.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete attachment {attachment.id}: {error.title}")
