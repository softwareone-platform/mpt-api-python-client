import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import assert_service_filter_with_iterate

pytestmark = [pytest.mark.flaky]


@pytest.mark.skip(reason="Not implemented yet")
def test_create(units_of_measure_service, short_uuid):
    units_of_measure_service.create({
        "name": f"e2e-delete {short_uuid}",
        "description": "e2e-delete",
    })  # act


def test_get_unit_of_measure(units_of_measure_service, unit_of_measure_id):
    result = units_of_measure_service.get(unit_of_measure_id)

    assert result.id == unit_of_measure_id


def test_filter_units_of_measure(units_of_measure_service, unit_of_measure_id):
    assert_service_filter_with_iterate(
        units_of_measure_service,
        unit_of_measure_id,
        ["-description"],
    )  # act


def test_get_unit_of_measure_not_found(units_of_measure_service):
    bogus_id = "UOM-0000-NOTFOUND"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        units_of_measure_service.get(bogus_id)


def test_update_unit_of_measure(units_of_measure_service, unit_of_measure_id, short_uuid):
    name = f"e2e-seeded-{short_uuid}"

    result = units_of_measure_service.update(
        unit_of_measure_id, {"name": name, "description": name}
    )

    assert result.name == name
