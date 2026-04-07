import pytest

from tests.e2e.helper import assert_async_service_filter_with_iterate

pytestmark = [pytest.mark.flaky]


async def test_filter_extension_installations(async_extension_installations_service, extension_id):
    await assert_async_service_filter_with_iterate(
        async_extension_installations_service, extension_id, None
    )  # act
