import pytest

from mpt_api_client import MPTClient
from mpt_api_client.exceptions import MPTHttpError


@pytest.mark.flaky
def test_unauthorised(base_url):
    client = MPTClient.from_config(api_token="TKN-invalid", base_url=base_url)  # noqa: S106

    with pytest.raises(MPTHttpError, match=r"401 Unauthorized"):
        client.catalog.products.fetch_page()


@pytest.mark.flaky
def test_access(mpt_vendor, product_id):
    result = mpt_vendor.catalog.products.get(product_id)

    assert result.id == product_id
