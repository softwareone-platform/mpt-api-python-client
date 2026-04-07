import pytest

from mpt_api_client.exceptions import MPTAPIError


@pytest.fixture(scope="session")
def extension_id(e2e_config):
    return e2e_config["integration.extension.id"]


@pytest.fixture(scope="session")
def term_id(e2e_config):
    return e2e_config["integration.term.id"]


@pytest.fixture
def extension_term_variants_service(mpt_ops, extension_id, term_id):
    return mpt_ops.integration.extensions.terms(extension_id).variants(term_id)


@pytest.fixture
def async_extension_term_variants_service(async_mpt_ops, extension_id, term_id):
    return async_mpt_ops.integration.extensions.terms(extension_id).variants(term_id)


@pytest.fixture
def variant_data(short_uuid):
    return {
        "type": "Online",
        "assetUrl": "https://example.com/terms",
        "languageCode": "en",
        "name": f"e2e - please delete {short_uuid}",
        "description": "Created by automated E2E tests. Safe to delete.",
    }


@pytest.fixture
def created_variant(extension_term_variants_service, variant_data):
    variant = extension_term_variants_service.create(variant_data)

    yield variant

    try:
        extension_term_variants_service.delete(variant.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete variant {variant.id}: {error.title}")  # noqa: WPS421


@pytest.fixture
async def async_created_variant(async_extension_term_variants_service, variant_data):
    variant = await async_extension_term_variants_service.create(variant_data)

    yield variant

    try:
        await async_extension_term_variants_service.delete(variant.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete variant {variant.id}: {error.title}")  # noqa: WPS421
