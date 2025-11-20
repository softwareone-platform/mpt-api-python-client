import pytest


@pytest.fixture
def media_data():
    return {
        "name": "e2e test media - please delete",
        "description": "E2E test media for automated testing",
        "displayOrder": 1,
        "type": "Image",
        "mediatype": "Image",
        "url": "",
        "language": "en-gb",
    }


@pytest.fixture
def test_media_file(logo_fd):
    return logo_fd
