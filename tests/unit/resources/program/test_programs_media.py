import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.program.programs_media import (
    AsyncMediaService,
    Media,
    MediaService,
)


@pytest.fixture
def media_service(http_client) -> MediaService:
    return MediaService(http_client=http_client, endpoint_params={"program_id": "PRG-001"})


@pytest.fixture
def async_media_service(async_http_client) -> AsyncMediaService:
    return AsyncMediaService(
        http_client=async_http_client, endpoint_params={"program_id": "PRG-001"}
    )


@pytest.fixture
def media_data():
    return {
        "id": "PMD-001",
        "name": "Program Dummy Video",
        "type": "Video",
        "description": "Dummy video for the program",
        "status": "Active",
        "filename": "intro.mp4",
        "size": 10485760,
        "contentType": "video/mp4",
        "displayOrder": 1,
        "url": "https://example.com/intro.mp4",
        "program": {"id": "PRG-001", "name": "Dummy Program"},
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_endpoint(media_service):
    result = media_service.path == "/public/v1/program/programs/PRG-001/media"

    assert result is True


def test_async_endpoint(async_media_service):
    result = async_media_service.path == "/public/v1/program/programs/PRG-001/media"

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "delete", "update", "download", "publish", "unpublish", "iterate"],
)
def test_methods_present(media_service, method):
    result = hasattr(media_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "delete", "update", "download", "publish", "unpublish", "iterate"],
)
def test_async_methods_present(async_media_service, method):
    result = hasattr(async_media_service, method)

    assert result is True


def test_media_primitive_fields(media_data):
    result = Media(media_data)

    assert result.to_dict() == media_data


def test_media_inherited_primitive_fields(media_inherited_data):
    result = Media(media_inherited_data)

    assert result.to_dict() == media_inherited_data


def test_media_nested_fields_are_base_models(media_data):
    result = Media(media_data)

    assert isinstance(result.program, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_media_optional_fields_absent():
    result = Media({"id": "PMD-001"})

    assert result.id == "PMD-001"
    assert result.name is None
    assert result.type is None
    assert result.description is None
    assert result.status is None
    assert result.filename is None
    assert result.size is None
    assert result.content_type is None
    assert result.display_order is None
    assert result.url is None
    assert result.program is None
    assert result.audit is None
