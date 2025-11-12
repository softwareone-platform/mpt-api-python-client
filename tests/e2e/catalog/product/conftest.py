import pathlib

import pytest


@pytest.fixture
def product_icon():
    icon_path = pathlib.Path(__file__).parents[2] / "logo.png"
    return pathlib.Path.open(icon_path, "rb")


@pytest.fixture
def product_data():
    return {"name": "Test Product", "website": "https://www.example.com"}
