from typing import Any, ClassVar

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model


class Parameter(Model):
    """Parameter resource."""

    _attribute_mapping: ClassVar[dict[str, str]] = {"externalId": "external_id"}

    @property
    def type_(self) -> str:
        """Returns the parameter type."""
        return str(self._box.get("type", ""))  # type: ignore[no-untyped-call]

    @type_.setter
    def type_(self, value: str) -> None:
        """Sets the parameter type."""
        self._box.type = value

    @property
    def scope(self) -> str:
        """Returns the parameter scope."""
        return str(self._box.get("scope", ""))  # type: ignore[no-untyped-call]

    @scope.setter
    def scope(self, value: str) -> None:
        """Sets the parameter scope."""
        self._box.scope = value

    @property
    def phase(self) -> str:
        """Returns the parameter phase."""
        return str(self._box.get("phase", ""))  # type: ignore[no-untyped-call]

    @phase.setter
    def phase(self, value: str) -> None:
        """Sets the parameter phase."""
        self._box.phase = value

    @property
    def context(self) -> str:
        """Returns the parameter context."""
        return str(self._box.get("context", ""))  # type: ignore[no-untyped-call]

    @context.setter
    def context(self, value: str) -> None:
        """Sets the parameter context."""
        self._box.context = value

    @property
    def options(self) -> dict[str, Any]:
        """Returns the parameter options."""
        return self._box.get("options", {})  # type: ignore[no-any-return, no-untyped-call]

    @options.setter
    def options(self, value: dict[str, Any]) -> None:
        """Sets the parameter options."""
        self._box.options = value

    @property
    def multiple(self) -> bool:
        """Returns whether the parameter allows multiple values."""
        return bool(self._box.get("multiple", False))  # type: ignore[no-untyped-call]

    @multiple.setter
    def multiple(self, value: bool) -> None:
        """Sets whether the parameter allows multiple values."""
        self._box.multiple = value

    @property
    def constraints(self) -> dict[str, Any]:
        """Returns the parameter constraints."""
        return self._box.get("constraints", {})  # type: ignore[no-any-return, no-untyped-call]

    @constraints.setter
    def constraints(self, value: dict[str, Any]) -> None:
        """Sets the parameter constraints."""
        self._box.constraints = value

    @property
    def group(self) -> dict[str, Any]:
        """Returns the parameter group."""
        return self._box.get("group", {})  # type: ignore[no-any-return,no-untyped-call]

    @group.setter
    def group(self, value: dict[str, Any]) -> None:
        """Sets the parameter group."""
        self._box.group = value

    @property
    def external_id(self) -> str:
        """Returns the parameter external ID."""
        return str(self._box.get("external_id", ""))  # type: ignore[no-untyped-call]

    @external_id.setter
    def external_id(self, value: str) -> None:
        """Sets the parameter external ID."""
        self._box.external_id = value

    @property
    def status(self) -> str:
        """Returns the parameter status."""
        return str(self._box.get("status", ""))  # type: ignore[no-untyped-call]

    @status.setter
    def status(self, value: str) -> None:
        """Sets the parameter status."""
        self._box.status = value


class ParametersServiceConfig:
    """Parameters service configuration."""

    _endpoint = "/public/v1/catalog/products/{product_id}/parameters"
    _model_class = Parameter
    _collection_key = "data"


class ParametersService(
    ManagedResourceMixin[Parameter],
    CollectionMixin[Parameter],
    Service[Parameter],
    ParametersServiceConfig,
):
    """Parameters service."""


class AsyncParametersService(
    AsyncManagedResourceMixin[Parameter],
    AsyncCollectionMixin[Parameter],
    AsyncService[Parameter],
    ParametersServiceConfig,
):
    """Parameters service."""
