import re
from collections import UserList
from collections.abc import Iterable
from types import MappingProxyType
from typing import Any, Self, get_args, get_origin, override

from mpt_api_client.http.types import Response
from mpt_api_client.models.meta import Meta
from mpt_api_client.models.model_collection import ModelCollection

ResourceData = dict[str, Any]


_SNAKE_CASE_BOUNDARY = re.compile(r"([a-z0-9])([A-Z])")
_SNAKE_CASE_ACRONYM = re.compile(r"(?<=[A-Z])(?=[A-Z][a-z0-9])")

# Explicit bidirectional mappings for API field names that contain two or more consecutive
# uppercase letters (e.g. PPx1, unitLP). The generic regex cannot round-trip these correctly,
# so we maintain an explicit lookup table that is checked before the regex is applied.
_FIELD_NAME_MAPPINGS: MappingProxyType[str, str] = MappingProxyType({
    # PP* price columns
    "PPx1": "ppx1",
    "PPxM": "ppxm",
    "PPxY": "ppxy",
    # SP* price columns
    "SPx1": "spx1",
    "SPxM": "spxm",
    "SPxY": "spxy",
    # LP* price columns
    "LPx1": "lpx1",
    "LPxM": "lpxm",
    "LPxY": "lpxy",
    # unit + 2-letter acronym suffix
    "unitLP": "unit_lp",
    "unitPP": "unit_pp",
    "unitSP": "unit_sp",
    # total + 2-letter acronym suffix
    "totalGT": "total_gt",
    "totalPP": "total_pp",
    "totalSP": "total_sp",
    "totalST": "total_st",
})

_FIELD_NAME_MAPPINGS_REVERSE: MappingProxyType[str, str] = MappingProxyType({
    snake: camel for camel, snake in _FIELD_NAME_MAPPINGS.items()
})


def to_snake_case(key: str) -> str:
    """Converts a camelCase string to snake_case.

    Explicit mappings in ``_FIELD_NAME_MAPPINGS`` take priority over the generic
    regex for fields that contain two or more consecutive uppercase letters.
    """
    mapped = _FIELD_NAME_MAPPINGS.get(key)
    if mapped is not None:
        return mapped
    if "_" in key and key.islower():
        return key
    # Common pattern for PascalCase/camelCase conversion
    snake = _SNAKE_CASE_BOUNDARY.sub(r"\1_\2", key)
    snake = _SNAKE_CASE_ACRONYM.sub(r"_", snake)
    return snake.lower().replace("__", "_")


def to_camel_case(key: str) -> str:
    """Converts a snake_case string to camelCase.

    Explicit mappings in ``_FIELD_NAME_MAPPINGS_REVERSE`` take priority over the
    generic logic for fields that contain two or more consecutive uppercase letters.
    """
    mapped = _FIELD_NAME_MAPPINGS_REVERSE.get(key)
    if mapped is not None:
        return mapped
    parts = key.split("_")
    return parts[0] + "".join(x.title() for x in parts[1:])  # noqa: WPS111 WPS221


class ModelList(UserList[Any]):
    """A list that automatically converts dictionaries to BaseModel objects."""

    def __init__(
        self,
        iterable: Iterable[Any] | None = None,
        model_class: type["BaseModel"] | None = None,  # noqa: WPS221
    ) -> None:
        self._model_class = model_class or BaseModel
        iterable = iterable or []
        super().__init__([self._process_item(item) for item in iterable])

    @override
    def append(self, item: Any) -> None:
        self.data.append(self._process_item(item))

    @override
    def extend(self, iterable: Iterable[Any]) -> None:
        self.data.extend(self._process_item(item) for item in iterable)

    @override
    def insert(self, index: Any, item: Any) -> None:
        self.data.insert(index, self._process_item(item))

    @override
    def __setitem__(self, index: Any, item: Any) -> None:
        self.data[index] = self._process_item(item)

    def _process_item(self, item: Any) -> Any:
        if isinstance(item, dict) and not isinstance(item, BaseModel):
            return self._model_class(**item)
        if isinstance(item, (list, UserList)) and not isinstance(item, ModelList):
            return ModelList(item, model_class=self._model_class)
        return item


class BaseModel:
    """Base dataclass for models providing object-only access and case conversion."""

    def __init__(self, **kwargs: Any) -> None:  # noqa: WPS210
        """Processes resource data to convert keys and handle nested structures."""
        # Get type hints for field mapping
        hints = getattr(self, "__annotations__", {})

        for key, value in kwargs.items():
            mapped_key = to_snake_case(key)

            # Check if there's a type hint for this key
            target_class = hints.get(mapped_key)
            processed_value = self._process_value(value, target_class=target_class)
            object.__setattr__(self, mapped_key, processed_value)

    def __getattr__(self, name: str) -> Any:
        # 1. Try to find the attribute in __dict__ (includes attributes set in __init__)
        if name in self.__dict__:
            return self.__dict__[name]  # noqa: WPS420 WPS529

        # 2. Check for methods or properties
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            pass  # noqa: WPS420

        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'",  # noqa: WPS237
        )

    @override
    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            object.__setattr__(self, name, value)
            return

        snake_name = to_snake_case(name)

        # Get target class for value processing if it's a known attribute
        hints = getattr(self, "__annotations__", {})
        target_class = hints.get(snake_name) or hints.get(name)

        processed_value = self._process_value(value, target_class=target_class)
        object.__setattr__(self, snake_name, processed_value)

    def to_dict(self) -> dict[str, Any]:
        """Returns the resource as a dictionary with original API keys."""
        out_dict = {}

        # Iterate over all attributes in __dict__ that aren't internal
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            if key == "meta":
                continue

            original_key = to_camel_case(key)
            out_dict[original_key] = self._serialize_value(value)

        return out_dict

    def _serialize_value(self, value: Any) -> Any:
        """Recursively serializes values back to dicts."""
        if isinstance(value, BaseModel):
            return value.to_dict()
        if isinstance(value, (list, UserList)):
            return [self._serialize_value(item) for item in value]
        return value

    def _process_value(self, value: Any, target_class: Any = None) -> Any:  # noqa: WPS231 C901
        """Recursively processes values to ensure nested dicts are BaseModels."""
        if isinstance(value, dict) and not isinstance(value, BaseModel):
            # If a target class is provided and it's a subclass of BaseModel, use it
            if (
                target_class
                and isinstance(target_class, type)
                and issubclass(target_class, BaseModel)
            ):
                return target_class(**value)
            return BaseModel(**value)

        if isinstance(value, (list, UserList)) and not isinstance(value, ModelList):
            # Try to determine the model class for the list elements from type hints
            model_class = BaseModel
            if target_class:
                # Handle list[ModelClass]

                origin = get_origin(target_class)
                if origin is list:
                    args = get_args(target_class)
                    if args and isinstance(args[0], type) and issubclass(args[0], BaseModel):  # noqa: WPS221
                        model_class = args[0]  # noqa: WPS220

            return ModelList(value, model_class=model_class)
        # Recursively handle BaseModel if it's already one
        if isinstance(value, BaseModel):
            return value
        return value


class Model(BaseModel):
    """Provides a resource to interact with api data using fluent interfaces."""

    id: str

    def __init__(
        self, resource_data: ResourceData | None = None, meta: Meta | None = None, **kwargs: Any
    ) -> None:
        object.__setattr__(self, "meta", meta)
        data = dict(resource_data or {})
        data.update(kwargs)
        super().__init__(**data)

    @override
    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"<{class_name} {self.id}>"

    @classmethod
    def from_response(cls, response: Response) -> Self | ModelCollection[Self]:
        """Creates a Model from a response.

        Args:
            response: The httpx response object.
        """
        response_data = response.json()

        if isinstance(response_data, dict):
            meta = Meta.from_response(response)
            response_data.pop("$meta", None)
            return cls(response_data, meta)
        if isinstance(response_data, list):
            return ModelCollection([cls(data_item) for data_item in response_data])

        raise TypeError(f"Incompatible response data type '{type(response_data).__name__}'.")
