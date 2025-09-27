import pytest

from mpt_api_client.resources.billing.credit_memos import (
    AsyncCreditMemosService,
    CreditMemosService,
)


@pytest.fixture
def credit_memos_service(http_client):
    return CreditMemosService(http_client=http_client)


@pytest.fixture
def async_credit_memos_service(async_http_client):
    return AsyncCreditMemosService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update"],
)
def test_mixins_present(credit_memos_service, method):
    assert hasattr(credit_memos_service, method)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update"],
)
def test_async_mixins_present(async_credit_memos_service, method):
    assert hasattr(async_credit_memos_service, method)
