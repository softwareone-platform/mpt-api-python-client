import pytest

from mpt_api_client.http.mixins import (
    AsyncManagedResourceMixin,
    AsyncModifiableResourceMixin,
    ManagedResourceMixin,
    ModifiableResourceMixin,
)
from tests.unit.conftest import DummyModel


class _ModifiableResourceService(ModifiableResourceMixin[DummyModel]):
    """Dummy service class for testing required methods."""


class _AsyncModifiableResourceService(AsyncModifiableResourceMixin[DummyModel]):
    """Dummy service class for testing required methods."""


class _ManagedService(ManagedResourceMixin[DummyModel]):
    """Dummy service class for testing required methods."""


class _AsyncManagedService(AsyncManagedResourceMixin[DummyModel]):
    """Dummy service class for testing required methods."""


@pytest.mark.parametrize(
    "method_name",
    [
        "update",
        "delete",
        "get",
    ],
)
def test_modifieable_resource_mixin(method_name: str) -> None:
    """Test that ModifiableResourceMixin has the required methods."""
    result = _ModifiableResourceService()

    assert hasattr(result, method_name), f"ModifiableResourceMixin should have {method_name} method"
    assert callable(getattr(result, method_name)), f"{method_name} should be callable"


@pytest.mark.parametrize(
    "method_name",
    [
        "update",
        "delete",
        "get",
    ],
)
def test_async_modifiable_resource_mixin(method_name: str) -> None:
    """Test that AsyncModifiableResourceMixin has the required methods."""
    result = _AsyncModifiableResourceService()

    assert hasattr(result, method_name), (
        f"AsyncModifiableResourceMixin should have {method_name} method"
    )
    assert callable(getattr(result, method_name)), f"{method_name} should be callable"


@pytest.mark.parametrize(
    "method_name",
    [
        "create",
        "update",
        "delete",
        "get",
    ],
)
def test_managed_resource_mixin(method_name: str) -> None:
    """Test that ManagedResourceMixin has the required methods."""
    result = _ManagedService()

    assert hasattr(result, method_name), f"ManagedResourceMixin should have {method_name} method"
    assert callable(getattr(result, method_name)), f"{method_name} should be callable"


@pytest.mark.parametrize(
    "method_name",
    [
        "create",
        "update",
        "delete",
        "get",
    ],
)
def test_async_managed_resource_mixin(method_name: str) -> None:
    """Test that AsyncManagedResourceMixin has the required methods."""
    result = _AsyncManagedService()

    assert hasattr(result, method_name), (
        f"AsyncManagedResourceMixin should have {method_name} method"
    )
    assert callable(getattr(result, method_name)), f"{method_name} should be callable"
