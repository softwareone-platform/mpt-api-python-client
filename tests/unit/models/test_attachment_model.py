from mpt_api_client.models import AttachmentModel


class AttachmentModelDummy(AttachmentModel):
    """Dummy class for testing AttachmentModel."""


def test_attachment_absent_fields():  # noqa: WPS218
    result = AttachmentModelDummy({"id": "ATT-001"})

    assert result.id == "ATT-001"
    assert result.name is None
    assert result.type is None
    assert result.size is None
    assert result.description is None
    assert result.content_type is None


def test_attachment_populates_camel():  # noqa: WPS218
    resource_data = {
        "id": "ATT-001",
        "name": "doc.pdf",
        "type": "application/pdf",
        "size": 1024,
        "description": "A document",
        "contentType": "application/pdf",
    }

    result = AttachmentModelDummy(resource_data)

    assert result.name == "doc.pdf"
    assert result.type == "application/pdf"
    assert result.size == 1024
    assert result.description == "A document"
    assert result.content_type == "application/pdf"
    assert result.to_dict() == resource_data


def test_attachment_repr():
    result = AttachmentModelDummy({"id": "ATT-001"})

    assert repr(result) == "<AttachmentModelDummy ATT-001>"
