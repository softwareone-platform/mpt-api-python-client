from mpt_api_client.models import DocumentModel


class DocumentModelDummy(DocumentModel):
    """Dummy class for testing DocumentModel."""


def test_document_absent_fields():  # noqa: WPS218
    result = DocumentModelDummy({"id": "DOC-001"})

    assert result.id == "DOC-001"
    assert result.name is None
    assert result.type is None
    assert result.size is None
    assert result.description is None
    assert result.content_type is None
    assert result.status is None
    assert result.filename is None
    assert result.url is None


def test_document_populates_camel():
    resource_data = {
        "id": "DOC-001",
        "name": "User Guide",
        "type": "Document",
        "size": 4096,
        "description": "User guide document",
        "contentType": "application/pdf",
        "status": "Active",
        "filename": "guide.pdf",
        "url": "https://example.com/guide.pdf",
    }

    result = DocumentModelDummy(resource_data)

    assert result.name == "User Guide"
    assert result.status == "Active"
    assert result.filename == "guide.pdf"
    assert result.url == "https://example.com/guide.pdf"
    assert result.to_dict() == resource_data


def test_document_repr():
    result = DocumentModelDummy({"id": "DOC-001"})

    assert repr(result) == "<DocumentModelDummy DOC-001>"
