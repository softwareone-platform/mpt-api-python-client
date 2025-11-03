import collections
import json
import pathlib
from typing import Any

from mpt_api_client.models import Model


class Context(collections.UserDict[str, Any]):
    """Application context."""

    def get_string(self, key: str, default: str = "") -> str:
        """Get string value from context."""
        return str(self.get(key, default))

    def get_resource(self, namespace: str, resource_id: str | None = None) -> Model:  # noqa: WPS615
        """Get resource from context.

        Raises:
            ValueError: if resource not found or wrong type.
        """
        resource_id = resource_id or self.get_string(f"{namespace}.id")
        resource = self.get(f"{namespace}[{resource_id}]")
        if not isinstance(resource, Model):
            raise ValueError(f"Resource {resource_id} not found.")  # noqa: TRY004
        return resource

    def set_resource(self, namespace: str, resource: Model) -> None:  # noqa: WPS615
        """Save resource to context."""
        self[f"{namespace}[{resource.id}]"] = resource


def load_context(json_file: pathlib.Path, context: Context | None = None) -> Context:
    """Load context from JSON file.

    Args:
        json_file: JSON file path.
        context: Context instance.

    Returns:
        Context instance.

    """
    context = context or Context()
    with json_file.open("r", encoding="utf-8") as fd:
        existing_data = json.load(fd)
    context.update(existing_data)
    return context


def save_context(context: Context, json_file: pathlib.Path) -> None:
    """Save context to JSON file.

    Args:
        json_file: JSON file path.
        context: Context instance.
    """
    with json_file.open("w", encoding="utf-8") as fd:
        json.dump(context.data, fd, indent=4, default=str)
