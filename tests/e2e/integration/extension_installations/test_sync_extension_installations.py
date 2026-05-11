import pytest

from tests.e2e.helper import assert_service_filter_with_iterate

pytestmark = [
    pytest.mark.flaky,
]


def test_filter_extension_installations(extension_installations_service, installation_id):
    assert_service_filter_with_iterate(
        extension_installations_service, installation_id, None
    )  # act


def test_get_extension_installation(extension_installations_service, installation_id):
    result = extension_installations_service.get(installation_id)

    assert result.id == installation_id
