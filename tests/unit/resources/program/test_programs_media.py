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


def test_media_nested_fields_are_base_models(media_data):
    result = Media(media_data)

    assert isinstance(result.program, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_media_optional_fields_absent():
    result = Media({"id": "PMD-001"})

    assert result.id == "PMD-001"
    assert not hasattr(result, "name")
    assert not hasattr(result, "type")
    assert not hasattr(result, "description")
    assert not hasattr(result, "status")
    assert not hasattr(result, "filename")
    assert not hasattr(result, "size")
    assert not hasattr(result, "content_type")
    assert not hasattr(result, "audit")
