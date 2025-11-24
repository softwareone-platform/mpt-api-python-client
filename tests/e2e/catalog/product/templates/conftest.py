import pytest


@pytest.fixture
def template_payload():
    return {
        "name": "Test Template - delete",
        "description": "A template for testing",
        "content": "template content",
        "type": "OrderProcessing",
    }


@pytest.fixture
def template_id(e2e_config):
    return e2e_config["catalog.product.template.id"]
