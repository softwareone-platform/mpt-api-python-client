import random

import pytest

from mpt_api_client import MPTClient
from mpt_api_client.exceptions import MPTAPIError


@pytest.mark.flaky(reruns=5, reruns_delay=0.01)  # noqa: WPS432
@pytest.mark.e2e
def test_example():
    assert random.choice([True, False])  # noqa: S311


@pytest.mark.flaky
@pytest.mark.e2e
def test_unauthorised(base_url):
    client = MPTClient.from_config(api_token="TKN-invalid", base_url=base_url)  # noqa: S106

    with pytest.raises(MPTAPIError, match=r"401 Unauthorized"):
        client.catalog.products.fetch_page()


@pytest.mark.flaky
@pytest.mark.e2e
def test_access(mpt_client):
    product = mpt_client.catalog.products.get("PRD-1975-5250")
    assert product.id == "PRD-1975-5250"
    assert product.name == "Amazon Web Services"
