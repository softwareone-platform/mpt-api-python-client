from unittest.mock import Mock

from mpt_api_client.modules import OrderCollectionClient
from mpt_api_client.mpt import MPT


def test_mapped_module() -> None:
    mock_registry = Mock()
    mpt = MPT(base_url="https://test.example.com", api_key="test-key", registry=mock_registry)

    mpt.orders  # noqa: B018

    mock_registry.get.assert_called_once_with("orders")


def test_not_mapped_module() -> None:
    mock_registry = Mock()
    mpt = MPT(base_url="https://test.example.com", api_key="test-key", registry=mock_registry)

    mpt.non_existing_module  # noqa: B018

    mock_registry.get.assert_called_once_with("non_existing_module")


def test_subclient_orders_module():
    mpt = MPT(base_url="https://test.example.com", api_key="test-key")

    orders_client = mpt.commerce.orders

    assert isinstance(orders_client, OrderCollectionClient)
    assert orders_client.mpt_client == mpt.mpt_client
