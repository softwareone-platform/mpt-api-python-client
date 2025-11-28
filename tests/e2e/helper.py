from contextlib import asynccontextmanager, contextmanager

from mpt_api_client import RQLQuery
from mpt_api_client.exceptions import MPTAPIError


@asynccontextmanager
async def async_create_fixture_resource_and_delete(service, resource_data):
    resource = await service.create(resource_data)

    yield resource

    try:
        await service.delete(resource.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete resource {resource}: {error.title}")  # noqa:  WPS421


@contextmanager
def create_fixture_resource_and_delete(service, resource_data):
    resource = service.create(resource_data)

    yield resource

    try:
        service.delete(resource.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete resource {resource}: {error.title}")  # noqa:  WPS421


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
