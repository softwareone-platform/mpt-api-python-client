import pytest

from mpt_api_client.resources.billing.manual_overrides import (
    AsyncManualOverridesService,
    ManualOverridesService,
)


@pytest.fixture
def manual_overrides_service(http_client):
    return ManualOverridesService(http_client=http_client)


@pytest.fixture
def async_manual_overrides_service(http_client):
    return AsyncManualOverridesService(http_client=http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update"],
)
def test_mixins_present(manual_overrides_service, method):
    assert hasattr(manual_overrides_service, method)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update"],
)
def test_async_mixins_present(async_manual_overrides_service, method):
    assert hasattr(async_manual_overrides_service, method)
