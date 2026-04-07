import pytest

from mpt_api_client.exceptions import MPTAPIError


@pytest.fixture(scope="session")
def extension_id(e2e_config):
    return e2e_config["integration.extension.id"]


@pytest.fixture
def extension_terms_service(mpt_vendor, extension_id):
    return mpt_vendor.integration.extensions.terms(extension_id)


@pytest.fixture
def async_extension_terms_service(async_mpt_vendor, extension_id):
    return async_mpt_vendor.integration.extensions.terms(extension_id)


@pytest.fixture
def term_data(short_uuid):
    return {
        "name": f"e2e - please delete {short_uuid}",
        "description": "Created by automated E2E tests. Safe to delete.",
        "displayOrder": 1,
    }


@pytest.fixture
def created_term(extension_terms_service, term_data):
    term = extension_terms_service.create(term_data)

    yield term

    try:
        extension_terms_service.delete(term.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete term {term.id}: {error.title}")  # noqa: WPS421


@pytest.fixture
async def async_created_term(async_extension_terms_service, term_data):
    term = await async_extension_terms_service.create(term_data)

    yield term

    try:
        await async_extension_terms_service.delete(term.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete term {term.id}: {error.title}")  # noqa: WPS421
