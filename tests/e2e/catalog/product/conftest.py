import pathlib

import pytest


@pytest.fixture
def product_icon():
    icon_path = pathlib.Path(__file__).parents[2] / "logo.png"
    return pathlib.Path.open(icon_path, "rb")


@pytest.fixture
def product_data():
    return {"name": "Test Product", "website": "https://www.example.com"}


@pytest.fixture
def parameter_group_id(e2e_config):
    return e2e_config["catalog.product.parameter_group.id"]


@pytest.fixture
def parameter_id(e2e_config):
    return e2e_config["catalog.product.parameter.id"]
