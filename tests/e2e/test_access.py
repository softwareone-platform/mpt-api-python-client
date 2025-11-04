import pytest

from mpt_api_client import MPTClient
from mpt_api_client.exceptions import MPTAPIError


@pytest.mark.flaky
def test_unauthorised(base_url):
    client = MPTClient.from_config(api_token="TKN-invalid", base_url=base_url)  # noqa: S106

    with pytest.raises(MPTAPIError, match=r"401 Unauthorized"):
        client.catalog.products.fetch_page()


@pytest.mark.flaky
def test_access(mpt_vendor, product_id):
    product = mpt_vendor.catalog.products.get(product_id)
    assert product.id == product_id
