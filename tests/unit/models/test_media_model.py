from mpt_api_client.models import MediaModel


class MediaModelDummy(MediaModel):
    """Dummy class for testing MediaModel."""


def test_media_absent_fields():  # noqa: WPS218
    result = MediaModelDummy({"id": "MED-001"})

    assert result.id == "MED-001"
    assert result.name is None
    assert result.type is None
    assert result.size is None
    assert result.description is None
    assert result.content_type is None
    assert result.status is None
    assert result.filename is None
    assert result.display_order is None
    assert result.url is None


def test_media_populates_camel():
    resource_data = {
        "id": "MED-001",
        "name": "Screenshot",
        "type": "Image",
        "size": 512000,
        "description": "Product screenshot",
        "contentType": "image/png",
        "status": "Active",
        "filename": "screenshot.png",
        "displayOrder": 1,
        "url": "https://example.com/screenshot.png",
    }

    result = MediaModelDummy(resource_data)

    assert result.name == "Screenshot"
    assert result.status == "Active"
    assert result.display_order == 1
    assert result.url == "https://example.com/screenshot.png"
    assert result.to_dict() == resource_data


def test_media_repr():
    result = MediaModelDummy({"id": "MED-001"})

    assert repr(result) == "<MediaModelDummy MED-001>"
