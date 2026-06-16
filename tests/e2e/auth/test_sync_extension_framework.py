import pytest

pytestmark = [pytest.mark.flaky]


def test_extension_framework_authenticates_request(mpt_extension_framework, product_id):
    result = mpt_extension_framework.catalog.products.get(product_id)

    assert result.id == product_id
