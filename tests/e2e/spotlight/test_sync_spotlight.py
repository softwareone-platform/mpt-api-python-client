import pytest

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def spotlight_objects_service(mpt_vendor):
    return mpt_vendor.spotlight.objects


@pytest.fixture
def spotlight_objects_data(spotlight_objects_service):
    select = ["-total", "-top", "-query"]
    spotlight_objects = spotlight_objects_service.select(*select)
    return list(spotlight_objects.iterate())


def test_select_spotlight_objects(spotlight_objects_data):
    result = spotlight_objects_data

    assert len(result) > 0


def test_refresh_spotlight_objects_all(spotlight_objects_service):
    spotlight_objects_service.refresh(object_id="-")  # act


def test_refresh_spotlight_objects_specific(spotlight_objects_data, spotlight_objects_service):
    result = spotlight_objects_data[0] if spotlight_objects_data else None

    if result is not None:
        spotlight_objects_service.refresh(object_id=result.id)
    assert result is not None
