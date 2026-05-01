from mpt_api_client.models import FileResourceModel


class FileResourceModelDummy(FileResourceModel):
    """Dummy class for testing FileResourceModel."""


def test_file_resource_absent_fields():  # noqa: WPS218
    result = FileResourceModelDummy({"id": "FRM-001"})

    assert result.id == "FRM-001"
    assert result.name is None
    assert result.type is None
    assert result.size is None
    assert result.description is None
    assert result.content_type is None


def test_file_resource_populates_camel():  # noqa: WPS218
    resource_data = {
        "id": "FRM-001",
        "name": "file.pdf",
        "type": "Document",
        "size": 1024,
        "description": "A file",
        "contentType": "application/pdf",
    }

    result = FileResourceModelDummy(resource_data)

    assert result.name == "file.pdf"
    assert result.type == "Document"
    assert result.size == 1024
    assert result.description == "A file"
    assert result.content_type == "application/pdf"
    assert result.to_dict() == resource_data


def test_file_resource_repr():
    result = FileResourceModelDummy({"id": "FRM-001"})

    assert repr(result) == "<FileResourceModelDummy FRM-001>"
