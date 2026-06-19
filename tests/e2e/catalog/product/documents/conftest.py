import pytest


@pytest.fixture
def document_data():
    return {
        "name": "e2e test document - please delete",
        "description": "E2E test document for automated testing",
        "language": "en-gb",
        "url": "",
    }


@pytest.fixture
def vendor_document_service(mpt_vendor, created_product):
    return mpt_vendor.catalog.products.documents(created_product.id)


@pytest.fixture
def async_vendor_document_service(async_mpt_vendor, async_created_product):
    return async_mpt_vendor.catalog.products.documents(async_created_product.id)
