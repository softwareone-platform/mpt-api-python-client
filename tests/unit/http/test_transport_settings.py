import pytest
from httpx_retries import Retry

from mpt_api_client.http.transport_settings import (
    ENV_BASE_URL,
    RETRY_ALLOWED_METHODS,
    EnvTransportSettings,
    TransportSettings,
)
from tests.unit.conftest import API_URL


def test_retries_count_is_normalized_to_retry():
    settings = TransportSettings(base_url=API_URL, retries=3)  # act

    assert isinstance(settings.retries, Retry)
    assert settings.retry.total == 3
    assert set(settings.retry.allowed_methods) == set(RETRY_ALLOWED_METHODS)


def test_retries_retry_instance_is_used_as_is():
    custom_retry = Retry(total=2, backoff_factor=1.5)

    settings = TransportSettings(base_url=API_URL, retries=custom_retry)  # act

    assert settings.retry is custom_retry


def test_base_url_is_validated():
    settings = TransportSettings(base_url=f"{API_URL}/public/v1/")  # act

    assert settings.url == API_URL


def test_missing_base_url_raises():
    with pytest.raises(ValueError, match="Base URL is required"):  # act
        TransportSettings()


def test_env_transport_reads_base_url_from_env(monkeypatch):
    monkeypatch.setenv(ENV_BASE_URL, "https://env.example.com")

    settings = EnvTransportSettings()  # act

    assert settings.url == "https://env.example.com"


def test_env_transport_explicit_base_url_wins(monkeypatch):
    monkeypatch.setenv(ENV_BASE_URL, "https://env.example.com")

    settings = EnvTransportSettings(base_url="https://explicit.example.com")  # act

    assert settings.url == "https://explicit.example.com"


def test_env_transport_missing_env_raises(monkeypatch):
    monkeypatch.delenv(ENV_BASE_URL, raising=False)

    with pytest.raises(ValueError, match="Base URL is required"):  # act
        EnvTransportSettings()
