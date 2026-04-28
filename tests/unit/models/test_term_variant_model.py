from mpt_api_client.models import TermVariantModel


class TermVariantModelDummy(TermVariantModel):
    """Dummy class for testing TermVariantModel."""


def test_term_variant_absent_fields():  # noqa: WPS218
    result = TermVariantModelDummy({"id": "TRV-001"})

    assert result.id == "TRV-001"
    assert result.name is None
    assert result.type is None
    assert result.size is None
    assert result.description is None
    assert result.content_type is None
    assert result.asset_url is None
    assert result.language_code is None
    assert result.status is None
    assert result.filename is None
    assert result.file_id is None


def test_term_variant_populates_camel():
    resource_data = {
        "id": "TRV-001",
        "name": "English Variant",
        "type": "PDF",
        "size": 2048,
        "description": "English language variant",
        "contentType": "application/pdf",
        "assetUrl": "https://example.com/file.pdf",
        "languageCode": "en-US",
        "status": "Active",
        "filename": "terms.pdf",
        "fileId": "FILE-001",
    }

    result = TermVariantModelDummy(resource_data)

    assert result.name == "English Variant"
    assert result.asset_url == "https://example.com/file.pdf"
    assert result.language_code == "en-US"
    assert result.file_id == "FILE-001"
    assert result.to_dict() == resource_data


def test_term_variant_repr():
    result = TermVariantModelDummy({"id": "TRV-001"})

    assert repr(result) == "<TermVariantModelDummy TRV-001>"
