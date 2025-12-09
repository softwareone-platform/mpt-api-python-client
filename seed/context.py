import collections
import json
import logging
import pathlib
from typing import Any

from mpt_api_client.models import Model

logger = logging.getLogger(__name__)


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
        """
        Save a Model instance into the context under a namespaced key.
        
        Parameters:
            namespace (str): Namespace prefix used to build the storage key.
            resource (Model): Resource to store; its `id` attribute is used to form the key.
        """
        self[f"{namespace}[{resource.id}]"] = resource


def load_context(json_file: pathlib.Path, context: Context) -> None:
    """
    Load JSON data from a file and update the given Context in place.
    
    Parameters:
        json_file (pathlib.Path): Path to the JSON file to read (UTF-8).
        context (Context): Context instance to be updated with the loaded data.
    """
    with json_file.open("r", encoding="utf-8") as fd:
        existing_data = json.load(fd)
    context.update(existing_data)
    logger.info("Context loaded: %s", context.items())


def save_context(context: Context, json_file: pathlib.Path) -> None:
    """
    Write the context's data to the given JSON file using UTF-8 encoding.
    
    Parameters:
        context (Context): Context whose data will be serialized.
        json_file (pathlib.Path): Path to the output JSON file.
    """
    with json_file.open("w", encoding="utf-8") as fd:
        json.dump(context.data, fd, indent=4, default=str)