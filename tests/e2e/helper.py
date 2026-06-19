from contextlib import asynccontextmanager, contextmanager

from mpt_api_client import RQLQuery
from mpt_api_client.exceptions import MPTAPIError


async def _delete_async_resource(service, resource):
    try:
        await service.delete(resource.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete resource {resource}: {error.title}")  # noqa:  WPS421


def _delete_resource(service, resource):
    try:
        service.delete(resource.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete resource {resource}: {error.title}")  # noqa:  WPS421


async def _finalize_async_resource(finalize, resource, logger):
    try:
        await finalize(resource.id)
    except Exception:
        logger.warning("TEARDOWN - Unable to finalize resource %s", resource, exc_info=True)


def _finalize_resource(finalize, resource, logger):
    try:
        finalize(resource.id)
    except Exception:
        logger.warning("TEARDOWN - Unable to finalize resource %s", resource, exc_info=True)


@asynccontextmanager
async def async_create_fixture_resource_and_delete(service, resource_data, upload_file=None):
    if upload_file is None:
        resource = await service.create(resource_data)
    else:
        resource = await service.create(resource_data, file=upload_file)

    try:
        yield resource
    finally:
        await _delete_async_resource(service, resource)


@contextmanager
def create_fixture_resource_and_delete(service, resource_data, upload_file=None):
    if upload_file is None:
        resource = service.create(resource_data)
    else:
        resource = service.create(resource_data, file=upload_file)

    try:
        yield resource
    finally:
        _delete_resource(service, resource)


@asynccontextmanager
async def async_create_fixture_resource_and_finalize(service, resource_data, finalize, logger):
    """Create a resource, then transition it to a terminal state on teardown.

    ``finalize`` is the bound terminal-transition method (e.g. ``queues.disable`` or
    ``cases.complete``) and is invoked best-effort so a failed teardown never fails the test.
    """
    resource = await service.create(resource_data)

    try:
        yield resource
    finally:
        await _finalize_async_resource(finalize, resource, logger)


@contextmanager
def create_fixture_resource_and_finalize(service, resource_data, finalize, logger):
    """Create a resource, then transition it to a terminal state on teardown.

    ``finalize`` is the bound terminal-transition method (e.g. ``queues.disable`` or
    ``cases.complete``) and is invoked best-effort so a failed teardown never fails the test.
    """
    resource = service.create(resource_data)

    try:
        yield resource
    finally:
        _finalize_resource(finalize, resource, logger)


async def assert_async_service_filter_with_iterate(service, filter_by_id, select: list[str] | None):
    filtered = service.filter(RQLQuery(id=filter_by_id))
    if select:
        filtered = filtered.select(*select)

    result = [filtered_item async for filtered_item in filtered.iterate()]

    assert len(result) == 1
    assert result[0].id == filter_by_id


def assert_service_filter_with_iterate(service, filter_by_id, select: list[str] | None):
    filtered = service.filter(RQLQuery(id=filter_by_id))
    if select:
        filtered = filtered.select(*select)

    result = list(filtered.iterate())

    assert len(result) == 1
    assert result[0].id == filter_by_id


def assert_update_resource(service, resource_id, update_field, update_value):
    payload = {update_field: update_value}

    result = service.update(resource_id, payload)

    assert result.id == resource_id
    assert result.to_dict().get(update_field) == update_value


async def assert_async_update_resource(service, resource_id, update_field, update_value):
    payload = {update_field: update_value}

    result = await service.update(resource_id, payload)

    assert result.id == resource_id
    assert result.to_dict().get(update_field) == update_value
