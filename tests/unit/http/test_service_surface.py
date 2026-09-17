import inspect
import pkgutil
from importlib import import_module

import pytest

from mpt_api_client import resources
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncStreamingMixin,
    AsyncStreamJSONLMixin,
    CollectionMixin,
    StreamingMixin,
    StreamJSONLMixin,
)

PACKAGE = resources


def _resource_modules():
    """Import and yield every module under `mpt_api_client.resources`."""
    for module_info in pkgutil.walk_packages(PACKAGE.__path__, f"{PACKAGE.__name__}."):
        yield import_module(module_info.name)


def _service_classes():
    """Collect every class defined under `mpt_api_client.resources`, keyed by import path."""
    return {
        f"{member.__module__}.{name}": member
        for module in _resource_modules()
        for name, member in inspect.getmembers(module, inspect.isclass)
        if member.__module__.startswith(PACKAGE.__name__)
    }


COLLECTION_SERVICES = tuple(
    pytest.param(service, id=name)
    for name, service in sorted(_service_classes().items())
    if issubclass(service, CollectionMixin | AsyncCollectionMixin)
)


def test_collection_services_were_discovered():
    result = len(COLLECTION_SERVICES)

    assert result > 0


# CollectionMixin inherits StreamingMixin, so the platform streaming read reaches every
# collection service without being composed in explicitly. This walks the package rather
# than listing services, so a service added later is covered without editing the test.
@pytest.mark.parametrize("service", COLLECTION_SERVICES)
def test_collection_services_expose_snapshot(service):
    expected = (
        AsyncStreamingMixin.stream_snapshot
        if issubclass(service, AsyncCollectionMixin)
        else StreamingMixin.stream_snapshot
    )

    result = service.stream_snapshot

    assert result is expected


# The guard against a repeat of the 7.0.0 break: stream() belongs to the endpoint-specific
# JSONL contract and to nothing else, so a service carries it only by composing that mixin.
@pytest.mark.parametrize("service", COLLECTION_SERVICES)
def test_stream_belongs_to_the_jsonl_mixin(service):
    composes_jsonl = issubclass(service, StreamJSONLMixin | AsyncStreamJSONLMixin)

    result = hasattr(service, "stream")

    assert result is composes_jsonl


@pytest.mark.parametrize("service", COLLECTION_SERVICES)
def test_no_service_exposes_stream_jsonl(service):
    result = hasattr(service, "stream_jsonl")

    assert result is False
