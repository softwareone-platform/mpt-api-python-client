from collections.abc import Callable
from typing import Any

from mpt_api_client.http.collection import CollectionClientBase

ItemType = type[CollectionClientBase[Any, Any]]


class Registry:
    """Registry for MPT collection clients."""

    def __init__(self) -> None:
        self.items: dict[str, ItemType] = {}  # noqa: WPS110

    def __call__(self, keyname: str) -> Callable[[ItemType], ItemType]:
        """Decorator to register a CollectionBaseClient class.

        Args:
            keyname: The key to register the class under

        Returns:
            The decorator function

        Examples:
            registry = Registry()
            @registry("orders")
            class OrderCollectionClient(CollectionBaseClient):
                _endpoint = "/api/v1/orders"
                _resource_class = Order

            registry.get("orders") == OrderCollectionClient
        """

        def decorator(cls: ItemType) -> ItemType:
            self.register(keyname, cls)
            return cls

        return decorator

    def register(self, keyname: str, item: ItemType) -> None:  # noqa: WPS110
        """Register a collection client class with a keyname.

        Args:
            keyname: The key to register the client under
            item: The collection client class to register
        """
        self.items[keyname] = item

    def get(self, keyname: str) -> ItemType:
        """Get a registered collection client class by keyname.

        Args:
            keyname: The key to look up

        Returns:
            The registered collection client class

        Raises:
            KeyError: If keyname is not registered
        """
        if keyname not in self.items:
            raise KeyError(f"No collection client registered with keyname: {keyname}")
        return self.items[keyname]

    def list_keys(self) -> list[str]:
        """Get all registered keynames.

        Returns:
            List of all registered keynames
        """
        return list(self.items.keys())


commerce = Registry()
