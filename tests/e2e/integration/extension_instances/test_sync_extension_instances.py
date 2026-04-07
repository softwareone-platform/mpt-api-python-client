import pytest

from tests.e2e.helper import assert_service_filter_with_iterate

pytestmark = [
    pytest.mark.flaky,
]


@pytest.mark.skip(reason="returns 500 error")
def test_create_extension_instance(extension_instances_service, instance_data):
    result = extension_instances_service.create(instance_data)

    assert result.external_id == instance_data["externalId"]


def test_filter_extension_instances(extension_instances_service, instance_id):
    assert_service_filter_with_iterate(extension_instances_service, instance_id, None)  # act


def test_get_extension_instance(extension_instances_service, instance_id):
    result = extension_instances_service.get(instance_id)

    assert result.id == instance_id
