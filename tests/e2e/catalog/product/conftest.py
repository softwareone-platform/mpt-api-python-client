import pathlib

import pytest


@pytest.fixture
def product_icon():
    return pathlib.Path.open(pathlib.Path(__file__).parent / "logo.png", "rb")


@pytest.fixture
def product_data():
    return {"name": "Test Product", "website": "https://www.example.com"}
