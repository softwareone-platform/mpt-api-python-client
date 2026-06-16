import pytest

pytestmark = [pytest.mark.flaky]


async def test_extension_framework_authenticates_request(async_mpt_extension_framework, product_id):
    result = await async_mpt_extension_framework.catalog.products.get(product_id)

    assert result.id == product_id
