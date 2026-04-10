import pytest

from mpt_api_client.exceptions import MPTAPIError


@pytest.fixture(scope="session")
def extension_id(e2e_config):
    return e2e_config["integration.extension.id"]


@pytest.fixture
def extension_documents_service(mpt_vendor, extension_id):
    return mpt_vendor.integration.extensions.documents(extension_id)


@pytest.fixture
def async_extension_documents_service(async_mpt_vendor, extension_id):
    return async_mpt_vendor.integration.extensions.documents(extension_id)


@pytest.fixture
def document_data(short_uuid):
    return {
        "name": f"e2e - please delete {short_uuid}",
        "description": "Created by automated E2E tests. Safe to delete.",
        "language": "en-US",
        "documentType": "File",
    }


@pytest.fixture
def created_document(extension_documents_service, document_data, pdf_fd):
    document = extension_documents_service.create(document_data, file=pdf_fd)

    yield document

    try:
        extension_documents_service.delete(document.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete document {document.id}: {error.title}")  # noqa: WPS421


@pytest.fixture
async def async_created_document(async_extension_documents_service, document_data, pdf_fd):
    document = await async_extension_documents_service.create(document_data, file=pdf_fd)

    yield document

    try:
        await async_extension_documents_service.delete(document.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete document {document.id}: {error.title}")  # noqa: WPS421
