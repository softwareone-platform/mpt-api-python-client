import pytest

from tests.e2e.helper import assert_service_filter_with_iterate

pytestmark = [
    pytest.mark.flaky,
]


def test_filter_extension_installations(extension_installations_service, extension_id):
    assert_service_filter_with_iterate(extension_installations_service, extension_id, None)  # act
