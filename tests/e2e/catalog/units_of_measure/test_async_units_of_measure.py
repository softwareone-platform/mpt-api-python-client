import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import assert_async_service_filter_with_iterate

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def async_units_of_measure_service(async_mpt_ops):
    return async_mpt_ops.catalog.units_of_measure


@pytest.mark.skip(reason="Not implemented yet")
async def test_create(async_units_of_measure_service, short_uuid):
    await async_units_of_measure_service.create({
        "name": f"e2e-delete {short_uuid}",
        "description": "e2e-delete",
    })  # act


async def test_get_unit_of_measure(async_units_of_measure_service, unit_of_measure_id):
    result = await async_units_of_measure_service.get(unit_of_measure_id)

    assert result.id == unit_of_measure_id


async def test_filter_units_of_measure(async_units_of_measure_service, unit_of_measure_id):
    await assert_async_service_filter_with_iterate(
        async_units_of_measure_service, unit_of_measure_id, ["-description"]
    )  # act


async def test_get_unit_of_measure_not_found(async_units_of_measure_service):
    bogus_id = "UOM-0000-NOTFOUND"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_units_of_measure_service.get(bogus_id)


async def test_update_unit_of_measure(
    async_units_of_measure_service, unit_of_measure_id, short_uuid
):
    name = f"e2e-seeded-{short_uuid}"

    result = await async_units_of_measure_service.update(
        unit_of_measure_id, {"name": name, "description": name}
    )

    assert result.name == name
