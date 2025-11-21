import pytest


@pytest.fixture
def document_id(e2e_config):
    return e2e_config["catalog.product.document.id"]


@pytest.fixture
def document_data():
    return {
        "name": "e2e test document - please delete",
        "description": "E2E test document for automated testing",
        "language": "en-gb",
        "url": "",
    }


@pytest.fixture
def vendor_document_service(mpt_vendor, product_id):
    return mpt_vendor.catalog.products.documents(product_id)


@pytest.fixture
def async_vendor_document_service(async_mpt_vendor, product_id):
    return async_mpt_vendor.catalog.products.documents(product_id)
