import pytest

from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.models import Model

API_TOKEN = "test-token"
API_URL = "https://api.example.com"


class DummyModel(Model):
    """Dummy resource for testing."""


@pytest.fixture
def http_client():
    return HTTPClient(base_url=API_URL, api_token=API_TOKEN)


@pytest.fixture
def async_http_client():
    return AsyncHTTPClient(base_url=API_URL, api_token=API_TOKEN)


@pytest.fixture
def attachment_data():
    return {
        "id": "ATT-001",
        "name": "attachment.pdf",
        "type": "Document",
        "size": 2048,
        "description": "Attachment description",
        "contentType": "application/pdf",
    }


@pytest.fixture
def document_inherited_data():
    return {
        "id": "DOC-001",
        "name": "User Guide",
        "type": "Document",
        "description": "User guide document",
        "status": "Active",
        "filename": "guide.pdf",
        "size": 4096,
        "contentType": "application/pdf",
        "url": "https://example.com/guide.pdf",
    }


@pytest.fixture
def media_inherited_data():
    return {
        "id": "MED-001",
        "name": "Screenshot",
        "type": "Image",
        "description": "Product screenshot",
        "status": "Active",
        "filename": "screenshot.png",
        "size": 512000,
        "contentType": "image/png",
        "displayOrder": 1,
        "url": "https://example.com/screenshot.png",
    }


@pytest.fixture
def term_variant_inherited_data():
    return {
        "id": "TRV-001",
        "name": "English Variant",
        "type": "PDF",
        "assetUrl": "https://example.com/file.pdf",
        "languageCode": "en-US",
        "description": "English language variant",
        "status": "Active",
        "filename": "terms.pdf",
        "size": 2048,
        "contentType": "application/pdf",
        "fileId": "FILE-001",
    }
