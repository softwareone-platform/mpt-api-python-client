import pytest

from mpt_api_client import (
    BearerTokenAuthentication,
    ExtensionFrameworkAuthentication,
    MPTClient,
)
from mpt_api_client.exceptions import MPTHttpError


@pytest.mark.flaky
def test_unauthorised(base_url):
    client = MPTClient.from_config(
        authentication=BearerTokenAuthentication("TKN-invalid"),
        base_url=base_url,
    )

    with pytest.raises(MPTHttpError, match=r"401 Authentication Failed"):
        client.catalog.products.fetch_page()


@pytest.mark.flaky
def test_access(mpt_vendor, product_id):
    result = mpt_vendor.catalog.products.get(product_id)

    assert result.id == product_id


@pytest.mark.flaky
def test_extension_framework_access(
    extension_secret, installation_account_id, base_url, product_id
):
    client = MPTClient.from_config(
        authentication=ExtensionFrameworkAuthentication(
            secret=extension_secret, account_id=installation_account_id
        ),
        base_url=base_url,
    )

    result = client.catalog.products.get(product_id)

    assert result.id == product_id
