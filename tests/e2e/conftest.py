import os

import pytest

from mpt_api_client import MPTClient


@pytest.fixture
def api_token():
    return os.getenv("MPT_API_TOKEN")


@pytest.fixture
def base_url():
    return os.getenv("MPT_API_BASE_URL")


@pytest.fixture
def mpt_client(api_token, base_url):
    return MPTClient.from_config(api_token=api_token, base_url=base_url)
