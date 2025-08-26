from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.mpt_client import AsyncMPTClient, MPTClient
from mpt_api_client.resources import AsyncCommerce, Commerce


def test_mpt_client() -> None:
    mpt = MPTClient(base_url="https://test.example.com", api_key="test-key")
    commerce = mpt.commerce

    assert isinstance(mpt, MPTClient)
    assert isinstance(commerce, Commerce)


def test_mpt_client_env(monkeypatch):
    monkeypatch.setenv("MPT_URL", "https://test.example.com")
    monkeypatch.setenv("MPT_TOKEN", "test-key")

    mpt = MPTClient()

    assert isinstance(mpt, MPTClient)
    assert isinstance(mpt.http_client, HTTPClient)


def test_async_mpt_client() -> None:
    mpt = AsyncMPTClient(base_url="https://test.example.com", api_key="test-key")
    commerce = mpt.commerce

    assert isinstance(mpt, AsyncMPTClient)
    assert isinstance(commerce, AsyncCommerce)


def test_async_mpt_client_env(monkeypatch):
    monkeypatch.setenv("MPT_URL", "https://test.example.com")
    monkeypatch.setenv("MPT_TOKEN", "test-key")

    mpt = AsyncMPTClient()

    assert isinstance(mpt, AsyncMPTClient)
    assert isinstance(mpt.http_client, AsyncHTTPClient)
