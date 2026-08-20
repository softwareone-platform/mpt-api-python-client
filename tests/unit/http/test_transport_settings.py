import pytest
from httpx_retries import Retry

from mpt_api_client.http.transport_settings import (
    DEFAULT_STREAM_READ_TIMEOUT,
    DEFAULT_TIMEOUT,
    ENV_BASE_URL,
    RETRY_ALLOWED_METHODS,
    EnvTransportSettings,
    TransportSettings,
)
from tests.unit.conftest import API_URL

PHASE_ONE_FIRST_BYTE_SLO = 60.0


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


def test_request_timeout_defaults_all_phases():
    settings = TransportSettings(base_url=API_URL)  # act

    request_timeout = settings.request_timeout
    assert request_timeout.connect == pytest.approx(DEFAULT_TIMEOUT)
    assert request_timeout.read == pytest.approx(DEFAULT_TIMEOUT)
    assert request_timeout.write == pytest.approx(DEFAULT_TIMEOUT)
    assert request_timeout.pool == pytest.approx(DEFAULT_TIMEOUT)


def test_timeout_is_the_fallback_for_unset_phases():
    settings = TransportSettings(base_url=API_URL, timeout=7.0, read_timeout=31.0)  # act

    request_timeout = settings.request_timeout
    assert request_timeout.read == pytest.approx(31.0)
    assert request_timeout.connect == pytest.approx(7.0)
    assert request_timeout.write == pytest.approx(7.0)
    assert request_timeout.pool == pytest.approx(7.0)


def test_phase_timeouts_set_independently():
    settings = TransportSettings(
        base_url=API_URL,
        connect_timeout=1.0,
        read_timeout=2.0,
        write_timeout=3.0,
        pool_timeout=4.0,
    )  # act

    request_timeout = settings.request_timeout
    assert request_timeout.connect == pytest.approx(1.0)
    assert request_timeout.read == pytest.approx(2.0)
    assert request_timeout.write == pytest.approx(3.0)
    assert request_timeout.pool == pytest.approx(4.0)


def test_stream_timeout_extends_read_phase_only():
    settings = TransportSettings(base_url=API_URL, timeout=9.0)  # act

    stream_timeout = settings.stream_timeout
    assert stream_timeout.read == pytest.approx(DEFAULT_STREAM_READ_TIMEOUT)
    assert stream_timeout.connect == pytest.approx(9.0)
    assert stream_timeout.write == pytest.approx(9.0)
    assert stream_timeout.pool == pytest.approx(9.0)


def test_stream_read_covers_deferred_byte():
    settings = TransportSettings(base_url=API_URL)  # act

    assert settings.request_timeout.read < PHASE_ONE_FIRST_BYTE_SLO
    assert settings.stream_timeout.read >= PHASE_ONE_FIRST_BYTE_SLO


def test_stream_read_timeout_is_configurable():
    settings = TransportSettings(base_url=API_URL, stream_read_timeout=600.0)  # act

    assert settings.stream_timeout.read == pytest.approx(600.0)


def test_stream_never_lowers_explicit_read():
    settings = TransportSettings(base_url=API_URL, read_timeout=900.0)  # act

    assert settings.stream_timeout.read == pytest.approx(900.0)
