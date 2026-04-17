import pytest


@pytest.fixture
def invalid_media_id():
    return "PMD-0000-0000-0000"


@pytest.fixture
def media_id(e2e_config):
    return e2e_config["program.media.id"]


@pytest.fixture
def media_data_factory():
    def factory(media_type: str = "Image"):
        return {
            "name": "E2E Created Program Media",
            "description": "E2E Created Program Media",
            "displayOrder": 1,
            "type": media_type,
            "mediatype": media_type,
            "url": "",
            "language": "en-us",
        }

    return factory
