"""Default dependency providers to avoid WPS404 violations."""

from dependency_injector.wiring import Provide

from seed.container import Container

# Constants for dependency injection to avoid WPS404 violations
DEFAULT_CONTEXT = Provide[Container.context]
DEFAULT_MPT_CLIENT = Provide[Container.mpt_client]
DEFAULT_MPT_VENDOR = Provide[Container.mpt_vendor]
DEFAULT_MPT_OPERATIONS = Provide[Container.mpt_operations]
