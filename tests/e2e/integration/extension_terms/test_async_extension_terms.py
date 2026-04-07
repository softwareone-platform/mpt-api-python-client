import pytest

from tests.e2e.helper import assert_async_service_filter_with_iterate

pytestmark = [
    pytest.mark.flaky,
]


def test_create_extension_term(async_created_term, term_data):
    result = async_created_term.name

    assert result == term_data["name"]


async def test_filter_extension_terms(async_extension_terms_service, async_created_term):
    await assert_async_service_filter_with_iterate(
        async_extension_terms_service, async_created_term.id, None
    )  # act


async def test_update_extension_term(async_extension_terms_service, async_created_term, short_uuid):
    update_data = {"name": f"e2e updated {short_uuid}"}

    result = await async_extension_terms_service.update(async_created_term.id, update_data)

    assert result.name == update_data["name"]


async def test_publish_extension_term(async_extension_terms_service, async_created_term):
    result = await async_extension_terms_service.publish(async_created_term.id)

    assert result.status == "Published"


async def test_unpublish_extension_term(async_extension_terms_service, async_created_term):
    await async_extension_terms_service.publish(async_created_term.id)

    result = await async_extension_terms_service.unpublish(async_created_term.id)

    assert result.status == "Unpublished"


async def test_delete_extension_term(async_extension_terms_service, async_created_term):
    await async_extension_terms_service.delete(async_created_term.id)  # act
